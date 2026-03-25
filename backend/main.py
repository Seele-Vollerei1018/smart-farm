# 智慧农业监测系统后端
# 基于FastAPI和CSV存储的原型实现

import os
import threading
import time
import uuid
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Literal, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import csv


# 配置参数
CSV_PATH = os.environ.get("SENSOR_CSV_PATH", os.path.join(".", "sensor_data.csv"))  # 传感器数据CSV文件路径
POLL_INTERVAL_SEC = float(os.environ.get("CSV_POLL_INTERVAL_SEC", "2.0"))  # 轮询间隔（秒）
ONLINE_DELTA_SEC = int(os.environ.get("DEVICE_OFFLINE_AFTER_SEC", "120"))  # 设备离线判断时间（秒）

# 线程锁
CSV_LOCK = threading.Lock()  # CSV文件操作锁
RULES_LOCK = threading.Lock()  # 规则操作锁

# 模拟数据配置
ENABLE_SIMULATION = os.environ.get("ENABLE_SENSOR_SIMULATION", "true").lower() == "true"  # 是否启用传感器数据模拟
SIM_POLL_INTERVAL_SEC = float(os.environ.get("SIM_POLL_INTERVAL_SEC", "2.0"))  # 模拟数据生成间隔（秒）


def _ensure_csv_header_if_missing(path: str) -> None:
    """
    确保CSV文件存在并包含正确的表头
    如果文件不存在或为空，则添加表头
    """
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature", "humidity", "light", "soil_moisture"])


def _append_row(row: Dict[str, Any]) -> None:
    """
    向CSV文件追加一行传感器数据
    """
    _ensure_csv_header_if_missing(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "temperature", "humidity", "light", "soil_moisture"])
        writer.writerow(row)


def _load_df() -> pd.DataFrame:
    """
    加载CSV文件数据为DataFrame
    包含时间戳解析和排序
    """
    # 注意：CSV可能被并发追加，需要使用CSV_LOCK保护
    with CSV_LOCK:
        _ensure_csv_header_if_missing(CSV_PATH)
        df = pd.read_csv(CSV_PATH)

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df = df.sort_values("timestamp")
    return df


def _get_latest_row(df: pd.DataFrame) -> Optional[pd.Series]:
    """
    获取DataFrame中的最新一行数据
    """
    if df.empty:
        return None
    return df.iloc[-1]


def _format_x_axis(ts_list: List[pd.Timestamp], range_value: str) -> List[str]:
    """
    根据时间范围格式化X轴标签
    24h范围显示小时:分钟，其他范围显示月-日 小时:分钟
    """
    if range_value == "24h":
        return [ts.strftime("%H:%M") for ts in ts_list]
    return [ts.strftime("%m-%d %H:%M") for ts in ts_list]


def _parse_interval(interval: str) -> str:
    """
    解析时间间隔字符串，转换为pandas支持的格式
    支持格式：1h, 30m, 1s等
    """
    unit = interval[-1].lower()
    n = float(interval[:-1]) if interval[:-1] else 1
    if unit == "h":
        # pandas offset aliases: '1H', '2H'
        return f"{int(n)}H"
    if unit == "m":
        return f"{int(n)}T"  # T == minutes
    if unit == "s":
        return f"{int(n)}S"
    raise HTTPException(status_code=400, detail=f"Unsupported interval: {interval}")


class RuleTrigger(BaseModel):
    """
    规则触发条件
    """
    sensor: Literal["soil_moisture", "temperature", "humidity", "light"]  # 传感器类型
    operator: Literal["<", ">", "<=", ">=", "=="]  # 操作符
    threshold: float  # 阈值


class RuleAction(BaseModel):
    """
    规则执行动作
    """
    device_target: str  # 目标设备
    command: str  # 执行命令
    duration: int = Field(60, ge=0)  # 执行持续时间（秒）


class RuleCreateRequest(BaseModel):
    """
    创建规则请求
    """
    rule_name: str  # 规则名称
    trigger: RuleTrigger  # 触发条件
    action: RuleAction  # 执行动作
    is_enabled: bool = True  # 是否启用


class RuleLogItem(BaseModel):
    """
    规则执行日志
    """
    timestamp: str  # 执行时间
    rule_name: str  # 规则名称
    trigger_value: str  # 触发值
    result: str  # 执行结果


class TelemetryUploadRequest(BaseModel):
    """
    遥测数据上传请求
    """
    device_sn: str  # 设备序列号
    auth_token: str  # 认证令牌
    data: Dict[str, Any]  # 传感器数据


# 创建FastAPI应用实例
app = FastAPI(title="Smart Farm Backend (CSV-based prototype)")

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)


# 全局变量
LATEST: Dict[str, Any] = {
    "temperature": None,  # 最新温度
    "humidity": None,  # 最新湿度
    "light": None,  # 最新光照
    "soil_moisture": None,  # 最新土壤湿度
    "timestamp": None,  # 最新数据时间戳
}

RULES: List[Dict[str, Any]] = []  # 规则列表
RULE_LOGS: List[Dict[str, Any]] = []  # 规则执行日志

_last_rule_eval_ts: Optional[datetime] = None  # 上次规则评估时间


def _eval_operator(value: float, operator: str, threshold: float) -> bool:
    """
    评估操作符条件
    判断传感器值是否满足规则条件
    """
    if operator == "<":
        return value < threshold
    if operator == ">":
        return value > threshold
    if operator == "<=":
        return value <= threshold
    if operator == ">=":
        return value >= threshold
    if operator == "==":
        return value == threshold
    return False


def _maybe_append_rule_log(sensor_value: float, rule: Dict[str, Any]) -> None:
    """
    添加规则执行日志
    """
    global RULE_LOGS
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trigger_value = str(sensor_value)
    action_cmd = rule["action"]["command"]
    log_item = {
        "timestamp": ts,
        "rule_name": rule["rule_name"],
        "trigger_value": trigger_value.strip(),
        "result": f"已执行: {action_cmd}",
    }
    RULE_LOGS.insert(0, log_item)
    # 保持日志大小合理
    RULE_LOGS = RULE_LOGS[:200]


def _rule_engine_tick() -> None:
    """
    规则引擎轮询函数
    定期检查传感器数据，评估规则条件，执行相应动作
    """
    global _last_rule_eval_ts
    while True:
        try:
            df = _load_df()
            if df.empty:
                time.sleep(POLL_INTERVAL_SEC)
                continue

            latest = _get_latest_row(df)
            if latest is None:
                time.sleep(POLL_INTERVAL_SEC)
                continue

            latest_ts: datetime = latest["timestamp"].to_pydatetime()
            # 快速更新最新数据缓存，用于设备状态
            LATEST["timestamp"] = latest_ts.strftime("%Y-%m-%d %H:%M:%S")
            LATEST["temperature"] = latest.get("temperature")
            LATEST["humidity"] = latest.get("humidity")
            LATEST["light"] = latest.get("light")
            LATEST["soil_moisture"] = latest.get("soil_moisture")

            if _last_rule_eval_ts is None:
                _last_rule_eval_ts = latest_ts
                time.sleep(POLL_INTERVAL_SEC)
                continue

            if latest_ts <= _last_rule_eval_ts:
                time.sleep(POLL_INTERVAL_SEC)
                continue

            # 评估自上次评估以来的新数据行
            new_rows = df[df["timestamp"] > pd.Timestamp(_last_rule_eval_ts)]
            if not new_rows.empty:
                with RULES_LOCK:
                    enabled_rules = [r for r in RULES if r.get("is_enabled")]
                    for _, row in new_rows.iterrows():
                        for rule in enabled_rules:
                            sensor_col = rule["trigger"]["sensor"]
                            sensor_value = row.get(sensor_col)
                            if sensor_value is None or pd.isna(sensor_value):
                                continue
                            if _eval_operator(float(sensor_value), rule["trigger"]["operator"], float(rule["trigger"]["threshold"])):
                                _maybe_append_rule_log(float(sensor_value), rule)

            _last_rule_eval_ts = latest_ts
        except Exception:
            # 避免后台线程崩溃
            pass

        time.sleep(POLL_INTERVAL_SEC)


def _sensor_simulation_tick() -> None:
    """
    传感器数据模拟函数
    在没有树莓派/真实传感器的情况下，生成模拟数据
    模拟数据会写入CSV，确保系统能够正常运行
    """
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 经验范围：可根据实际传感器标定调整
            base_temp = 24.0 + random.uniform(-1.2, 1.2)  # 温度范围：22.8-25.2℃
            base_humi = 70 + random.uniform(-4.0, 4.0)  # 湿度范围：66-74%
            base_light = 8200 + random.uniform(-700, 700)  # 光照范围：7500-8900 lux
            base_soil = 55 + random.uniform(-7.0, 7.0)  # 土壤湿度范围：48-62%

            row = {
                "timestamp": now,
                "temperature": int(round(base_temp)),
                "humidity": int(round(base_humi)),
                "light": int(round(max(0, base_light))),
                "soil_moisture": int(round(max(0, min(100, base_soil)))),
            }

            with CSV_LOCK:
                _append_row(row)
        except Exception:
            # 防止模拟线程异常退出
            pass

        time.sleep(SIM_POLL_INTERVAL_SEC)


def _clear_csv_daily() -> None:
    """
    每日清空CSV文件的函数
    每24小时清空一次sensor_data.csv文件，从第一行重新开始更新
    """
    while True:
        try:
            # 等待24小时
            time.sleep(24 * 60 * 60)
            
            # 清空CSV文件，只保留表头
            with CSV_LOCK:
                os.makedirs(os.path.dirname(CSV_PATH) or ".", exist_ok=True)
                with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["timestamp", "temperature", "humidity", "light", "soil_moisture"])
        except Exception:
            # 防止线程异常退出
            pass


@app.on_event("startup")
def _startup() -> None:
    """
    应用启动时的初始化函数
    启动后台线程：
    1. 规则引擎线程 - 定期检查传感器数据，评估规则
    2. 传感器模拟线程 - 生成模拟数据（如果启用）
    3. CSV清空线程 - 每24小时清空一次CSV文件
    """
    # 启动规则引擎线程，用于定期检查传感器数据和评估规则
    t = threading.Thread(target=_rule_engine_tick, daemon=True)
    t.start()

    # 如果启用了传感器模拟，启动模拟线程
    if ENABLE_SIMULATION:
        sim = threading.Thread(target=_sensor_simulation_tick, daemon=True)
        sim.start()
    
    # 启动每日清空CSV文件的线程
    clear_csv_thread = threading.Thread(target=_clear_csv_daily, daemon=True)
    clear_csv_thread.start()


@app.get("/api/v1/devices/{device_id}/status")
def get_device_status(device_id: str) -> Dict[str, Any]:
    """
    获取设备状态
    参数：
        device_id: 设备ID
    返回：
        设备状态信息，包括在线状态、最后活跃时间等
    """
    df = _load_df()
    latest = _get_latest_row(df)

    if latest is None:
        return {
            "code": 200,
            "data": {
                "device_id": device_id,
                "status": "offline",
                "last_active": None,
                "signal_strength": None,
                "battery_level": None,
            },
        }

    last_active_ts: datetime = latest["timestamp"].to_pydatetime()
    delta = datetime.now() - last_active_ts
    status = "online" if delta.total_seconds() <= ONLINE_DELTA_SEC else "offline"

    return {
        "code": 200,
        "data": {
            "device_id": device_id,
            "status": status,
            "last_active": last_active_ts.strftime("%Y-%m-%d %H:%M:%S"),
            "signal_strength": None,
            "battery_level": None,
        },
    }


@app.get("/api/v1/analytics/history")
def history(sensor_type: str, range: Literal["24h", "7d", "30d"] = "24h", interval: str = "1h") -> Dict[str, Any]:
    """
    获取传感器历史数据
    参数：
        sensor_type: 传感器类型（temperature, humidity, light, soil_moisture）
        range: 时间范围（24h, 7d, 30d）
        interval: 数据间隔（如1h, 30m等）
    返回：
        历史数据，包括时间轴、值轴、最小值和最大值
    """
    df = _load_df()
    if df.empty:
        return {"code": 200, "data": {"x_axis": [], "y_axis": [], "min_val": None, "max_val": None}}

    now = datetime.now()
    if range == "24h":
        start = now - timedelta(hours=24)
    elif range == "7d":
        start = now - timedelta(days=7)
    else:
        start = now - timedelta(days=30)

    sensor_col = sensor_type
    if sensor_col not in {"temperature", "humidity", "light", "soil_moisture"}:
        raise HTTPException(status_code=400, detail=f"Unsupported sensor_type: {sensor_type}")

    df = df[(df["timestamp"] >= pd.Timestamp(start)) & (df["timestamp"] <= pd.Timestamp(now))]
    if df.empty:
        return {"code": 200, "data": {"x_axis": [], "y_axis": [], "min_val": None, "max_val": None}}

    freq = _parse_interval(interval)
    df = df.set_index("timestamp")
    series = df[sensor_col].resample(freq).mean().dropna()

    x_axis_ts = list(series.index)
    y_axis = [float(v) for v in series.values]

    min_val = float(min(y_axis)) if y_axis else None
    max_val = float(max(y_axis)) if y_axis else None

    return {
        "code": 200,
        "data": {
            "x_axis": _format_x_axis(x_axis_ts, range),
            "y_axis": y_axis,
            "min_val": min_val,
            "max_val": max_val,
        },
    }


@app.post("/api/v1/rules/create")
def create_rule(req: RuleCreateRequest) -> Dict[str, Any]:
    """
    创建规则
    参数：
        req: 规则创建请求，包含规则名称、触发条件和执行动作
    返回：
        规则创建结果，包含规则ID
    """
    rule_id = f"rule_{uuid.uuid4().hex[:6]}"
    rule = {
        "rule_id": rule_id,
        "rule_name": req.rule_name,
        "trigger": req.trigger.model_dump(),
        "action": req.action.model_dump(),
        "is_enabled": req.is_enabled,
    }
    with RULES_LOCK:
        RULES.insert(0, rule)

    return {"code": 200, "msg": "规则创建成功", "rule_id": rule_id}


@app.get("/api/v1/rules/logs")
def rule_logs() -> Dict[str, Any]:
    """
    获取规则执行日志
    返回：
        规则执行日志列表
    """
    with RULES_LOCK:
        return {"code": 200, "data": list(RULE_LOGS)}


@app.post("/api/v1/telemetry/upload")
def telemetry_upload(req: TelemetryUploadRequest) -> Dict[str, Any]:
    """
    上传遥测数据
    如果后续选择从STM32->网关->后端发送数据，此端点可以直接将数据追加到CSV
    参数：
        req: 遥测数据上传请求，包含设备序列号、认证令牌和传感器数据
    返回：
        上传结果
    """
    data = req.data or {}
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "light": data.get("light"),
        "soil_moisture": data.get("soil_moisture"),
    }

    # 基本验证
    for k in ["temperature", "humidity", "light", "soil_moisture"]:
        if row[k] is None:
            raise HTTPException(status_code=400, detail=f"Missing field in data: {k}")

    with CSV_LOCK:
        _append_row(row)

    return {"code": 200, "msg": "success", "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "commands": []}


@app.get("/api/v1/analytics/report/export")
def export_report(format: Literal["pdf", "xlsx"] = "xlsx") -> Any:
    """
    导出分析报告
    参数：
        format: 导出格式（目前仅支持xlsx）
    返回：
        导出的Excel文件
    """
    if format != "xlsx":
        raise HTTPException(status_code=400, detail="Only xlsx export is implemented in this prototype.")

    df = _load_df()
    if df.empty:
        # 返回空Excel文件
        df = pd.DataFrame(columns=["timestamp", "temperature", "humidity", "light", "soil_moisture"])

    out_path = os.path.join(".", "report.xlsx")
    # 导出最近24小时的数据作为简单报告
    now = datetime.now()
    start = now - timedelta(hours=24)
    df2 = df[(df["timestamp"] >= pd.Timestamp(start)) & (df["timestamp"] <= pd.Timestamp(now))].copy()

    # 转换为Excel友好的格式
    if not df2.empty:
        df2["timestamp"] = df2["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    with CSV_LOCK:
        df2.to_excel(out_path, index=False)

    if not os.path.exists(out_path):
        raise HTTPException(status_code=500, detail="Export failed: file not created.")

    # 直接流式传输生成的XLSX文件
    return FileResponse(
        out_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="smart_farm_report.xlsx",
    )

