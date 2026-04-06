# smart-farm backend（原型）

这是一个用于“把 Raspberry Pi / STM32 采集到的 CSV 数据，提供给前端页面”的 FastAPI 后端原型。

## 你需要准备

1. 你的串口采集脚本会不断写入 CSV：`sensor_data.csv`
2. 请确保后端运行目录下能找到这个文件，或通过环境变量指定路径

## 安装依赖

在 `backend/` 目录创建虚拟环境并安装依赖（示例）：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

（如果在树莓派上运行，命令可能略有不同）

## 启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

后端默认会在没有树莓派/CSV 输入的情况下自动模拟传感器数据，确保页面接口可用。
如果你后续接上真实串口上报，需要关闭模拟即可：

```bash
set ENABLE_SENSOR_SIMULATION=false
```

如果你的 CSV 不在当前目录，设置：

```bash
set SENSOR_CSV_PATH=D:\path\to\sensor_data.csv
```

## 主要接口

- `GET /api/v1/devices/{id}/status`
- `GET /api/v1/analytics/history?sensor_type=temperature&range=24h&interval=1h`
- `POST /api/v1/rules/create`
- `GET /api/v1/rules/logs`
- `GET /api/v1/analytics/report/export?format=xlsx`（原型只实现 xlsx）

