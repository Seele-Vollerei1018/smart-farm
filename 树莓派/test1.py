
import serial
import time
import csv
import re
import requests
from datetime import datetime

SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 115200
TIMEOUT = 1

SERVER_URL = "http://8.138.40.5:8001/api/v1/telemetry/upload"
DEVICE_SN = "test001"
AUTH_TOKEN = "test"

def init_serial():
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=TIMEOUT
        )
        print(f"串口连接成功: {SERIAL_PORT} @ {BAUD_RATE}")
        return ser
    except Exception as e:
        print(f"串口初始化失败: {e}")
        return None

def extract_csv_line(text):
    """
    从混杂串口输出中提取形如:
    25,60,300,45
    的四字段纯数字 CSV
    """
    match = re.search(r'(\d+),(\d+),(\d+),(\d+)', text)
    if match:
        return match.group(0)
    return None

def parse_sensor_data(data_str):
    try:
        temp, humi, light, value = map(int, data_str.strip().split(','))
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": temp,
            "humidity": humi,
            "light": light,
            "soil_moisture": value
        }
    except Exception as e:
        print(f"数据解析失败: {e}, 原始数据: {data_str}")
        return None

def save_to_csv(data, filename="sensor_data.csv"):
    file_exists = False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ["timestamp", "temperature", "humidity", "light", "soil_moisture"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def send_to_server(data):
    payload = {
        "device_sn": DEVICE_SN,
        "auth_token": AUTH_TOKEN,
        "data": {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "light": data["light"],
            "soil_moisture": data["soil_moisture"]
        }
    }

    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        print("上传状态:", response.status_code)
        print("服务器返回:", response.text)
    except Exception as e:
        print("上传失败:", e)

def main():
    ser = init_serial()
    if not ser:
        return

    print("开始接收传感器数据 (按Ctrl+C停止)...")

    buffer = ""

    try:
        while True:
            raw = ser.read(ser.in_waiting or 1)
            if raw:
                # 忽略非法字节，避免直接报 UnicodeDecodeError
                text = raw.decode('utf-8', errors='ignore')
                buffer += text

                # 防止缓冲区无限变大
                if len(buffer) > 1000:
                    buffer = buffer[-500:]

                # 尝试从缓冲区中提取合法 CSV 数据
                line = extract_csv_line(buffer)
                if line:
                    sensor_data = parse_sensor_data(line)
                    if sensor_data:
                        print(f"\n[{sensor_data['timestamp']}]")
                        print(f"温度: {sensor_data['temperature']}°C")
                        print(f"湿度: {sensor_data['humidity']}%")
                        print(f"光照: {sensor_data['light']} lux")
                        print(f"土壤湿度: {sensor_data['soil_moisture']}")

                        save_to_csv(sensor_data)
                        send_to_server(sensor_data)

                    # 提取成功后清空缓冲，等待下一帧
                    buffer = ""

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("串口已关闭")

if __name__ == "__main__":
    main()