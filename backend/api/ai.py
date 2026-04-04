from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import call_qwen

router = APIRouter()


class AIRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(req: AIRequest):
    question = req.message.strip()

    if not question:
        raise HTTPException(status_code=400, detail="message 不能为空")

    result = call_qwen(question)

    return {
        "code": 200,
        "data": result
    }