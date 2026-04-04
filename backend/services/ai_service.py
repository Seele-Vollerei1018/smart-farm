from dotenv import load_dotenv
import os
import requests
from typing import Any, Dict

load_dotenv()

API_KEY = os.getenv("AI_API_KEY")

QWEN_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"


def call_qwen(question: str) -> str:
    """
    调用通义千问，返回字符串答案
    出错时直接抛异常，让 FastAPI 返回明确报错
    """

    if not API_KEY:
        raise RuntimeError("AI_API_KEY 未配置，请检查 .env 文件")

    payload: Dict[str, Any] = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是一个农业学习助手，面向中小学生。"
                        "请使用简单、友好、通俗易懂的中文回答。"
                        "尽量分点说明，不要使用过于专业的术语。"
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ]
        },
        "parameters": {
            "temperature": 0.7,
            "result_format": "text"
        }
    }

    try:
        res = requests.post(
            QWEN_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            json=payload,
            timeout=30,
        )
    except requests.RequestException as e:
        raise RuntimeError(f"调用通义接口失败：{e}")

    if res.status_code != 200:
        raise RuntimeError(f"通义接口异常 status={res.status_code}：{res.text}")

    try:
        data = res.json()
    except ValueError:
        raise RuntimeError(f"返回不是 JSON：{res.text}")

    text = data.get("output", {}).get("text")

    if text:
        return text

    raise RuntimeError(f"未返回有效内容：{data}")

