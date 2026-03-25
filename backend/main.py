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


CSV_PATH = os.environ.get("SENSOR_CSV_PATH", os.path.join(".", "sensor_data.csv"))
POLL_INTERVAL_SEC = float(os.environ.get("CSV_POLL_INTERVAL_SEC", "2.0"))
ONLINE_DELTA_SEC = int(os.environ.get("DEVICE_OFFLINE_AFTER_SEC", "120"))

CSV_LOCK = threading.Lock()
RULES_LOCK = threading.Lock()

ENABLE_SIMULATION = os.environ.get("ENABLE_SENSOR_SIMULATION", "true").lower() == "true"
SIM_POLL_INTERVAL_SEC = float(os.environ.get("SIM_POLL_INTERVAL_SEC", "2.0"))


def _ensure_csv_header_if_missing(path: str) -> None:
    # Ensure the writer can append safely even if the file is newly created.
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature", "humidity", "light", "soil_moisture"])


def _append_row(row: Dict[str, Any]) -> None:
    _ensure_csv_header_if_missing(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "temperature", "humidity", "light", "soil_moisture"])
        writer.writerow(row)


def _load_df() -> pd.DataFrame:
    # NOTE: CSV may be appended concurrently; we guard with CSV_LOCK.
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
    if df.empty:
        return None
    return df.iloc[-1]


def _format_x_axis(ts_list: List[pd.Timestamp], range_value: str) -> List[str]:
    if range_value == "24h":
        return [ts.strftime("%H:%M") for ts in ts_list]
    return [ts.strftime("%m-%d %H:%M") for ts in ts_list]


def _parse_interval(interval: str) -> str:
    # doc examples: "1h"
    # allow "30m", "1h" etc.
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
    sensor: Literal["soil_moisture", "temperature", "humidity", "light"]
    operator: Literal["<", ">", "<=", ">=", "=="]
    threshold: float


class RuleAction(BaseModel):
    device_target: str
    command: str
    duration: int = Field(60, ge=0)


class RuleCreateRequest(BaseModel):
    rule_name: str
    trigger: RuleTrigger
    action: RuleAction
    is_enabled: bool = True


class RuleLogItem(BaseModel):
    timestamp: str
    rule_name: str
    trigger_value: str
    result: str


class TelemetryUploadRequest(BaseModel):
    device_sn: str
    auth_token: str
    data: Dict[str, Any]


app = FastAPI(title="Smart Farm Backend (CSV-based prototype)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


LATEST: Dict[str, Any] = {
    "temperature": None,
    "humidity": None,
    "light": None,
    "soil_moisture": None,
    "timestamp": None,
}

RULES: List[Dict[str, Any]] = []
RULE_LOGS: List[Dict[str, Any]] = []

_last_rule_eval_ts: Optional[datetime] = None


def _eval_operator(value: float, operator: str, threshold: float) -> bool:
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
    # keep log size reasonable
    RULE_LOGS = RULE_LOGS[:200]


def _rule_engine_tick() -> None:
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
            # Update latest cache for device status quickly.
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

            # Evaluate rules for the new rows since last evaluation.
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
            # Avoid crashing the background thread.
            pass

        time.sleep(POLL_INTERVAL_SEC)


def _sensor_simulation_tick() -> None:
    """
    在没有树莓派/CSV 的情况下，让系统也能跑起来。
    模拟数据会写入 CSV，后续历史/状态/规则日志都能正常工作。
    """
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 经验范围：你后续可按实际传感器标定调整
            base_temp = 24.0 + random.uniform(-1.2, 1.2)
            base_humi = 70 + random.uniform(-4.0, 4.0)
            base_light = 8200 + random.uniform(-700, 700)
            base_soil = 55 + random.uniform(-7.0, 7.0)

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


@app.on_event("startup")
def _startup() -> None:
    # Start background polling for latest values and simple rule evaluation.
    t = threading.Thread(target=_rule_engine_tick, daemon=True)
    t.start()

    if ENABLE_SIMULATION:
        sim = threading.Thread(target=_sensor_simulation_tick, daemon=True)
        sim.start()


@app.get("/api/v1/devices/{device_id}/status")
def get_device_status(device_id: str) -> Dict[str, Any]:
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
    with RULES_LOCK:
        return {"code": 200, "data": list(RULE_LOGS)}


@app.post("/api/v1/telemetry/upload")
def telemetry_upload(req: TelemetryUploadRequest) -> Dict[str, Any]:
    # If you later choose to send data from STM32->gateway->backend,
    # this endpoint can directly append them into CSV.
    data = req.data or {}
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
        "light": data.get("light"),
        "soil_moisture": data.get("soil_moisture"),
    }

    # Basic validation.
    for k in ["temperature", "humidity", "light", "soil_moisture"]:
        if row[k] is None:
            raise HTTPException(status_code=400, detail=f"Missing field in data: {k}")

    with CSV_LOCK:
        _append_row(row)

    return {"code": 200, "msg": "success", "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "commands": []}


@app.get("/api/v1/analytics/report/export")
def export_report(format: Literal["pdf", "xlsx"] = "xlsx") -> Any:
    if format != "xlsx":
        raise HTTPException(status_code=400, detail="Only xlsx export is implemented in this prototype.")

    df = _load_df()
    if df.empty:
        # Return an empty excel.
        df = pd.DataFrame(columns=["timestamp", "temperature", "humidity", "light", "soil_moisture"])

    out_path = os.path.join(".", "report.xlsx")
    # Export last 24 hours as the simple report.
    now = datetime.now()
    start = now - timedelta(hours=24)
    df2 = df[(df["timestamp"] >= pd.Timestamp(start)) & (df["timestamp"] <= pd.Timestamp(now))].copy()

    # Convert to human-friendly format for Excel
    if not df2.empty:
        df2["timestamp"] = df2["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    with CSV_LOCK:
        df2.to_excel(out_path, index=False)

    if not os.path.exists(out_path):
        raise HTTPException(status_code=500, detail="Export failed: file not created.")

    # Stream the generated XLSX file directly.
    return FileResponse(
        out_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="smart_farm_report.xlsx",
    )

