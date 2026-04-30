"""
Middleware для инъекции сессии БД в обработчики.
Каждый запрос получает свою сессию, которая автоматически закрывается.
"""

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.engine import async_session_maker


class DbSessionMiddleware(BaseMiddleware):
    """
    Middleware, который создаёт AsyncSession для каждого обновления
    и передаёт её в data["session"] для использования в хендлерах.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            data["session"] = session
            return await handler(event, data)
