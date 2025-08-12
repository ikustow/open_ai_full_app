"""
Эндпоинт для обработки сообщений через агентов
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents import Runner, SQLiteSession
from agents_core.agents.route_agent import route_agent
from agents_core.agents.context.context_manager import ContextManager

router = APIRouter()


class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"
    user_id: str = "123_id"


class MessageResponse(BaseModel):
    response: str


@router.post("/", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    """Обработка сообщения через route_agent"""
    try:
        # Создаем сессию с встроенным менеджером базы данных
        session = SQLiteSession(request.session_id, "src/database/conversation_history.db")
        user_id = request.user_id
        # Создаем контекст-менеджер
        context_manager = ContextManager()
        
        # Обрабатываем сообщение через route_agent с передачей контекста
        result = await Runner.run(
            route_agent,
            request.message,
            session=session,
            context=context_manager
        )
        
        return MessageResponse(response=result.final_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки сообщения: {str(e)}")
