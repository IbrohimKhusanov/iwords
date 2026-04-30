"""
Middleware для инъекции сессии БД и локали пользователя в обработчики.
Каждый запрос получает свою сессию и locale, которые автоматически закрываются.
"""

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy import select

from database.engine import async_session_maker
from database.models import User


class DbSessionMiddleware(BaseMiddleware):
    """
    Middleware, который создаёт AsyncSession для каждого обновления
    и передаёт session, locale и user_db в data для использования в хендлерах.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            data["session"] = session

            # Определяем user_id из события
            user = data.get("event_from_user")
            if user:
                # Ищем пользователя в БД
                db_user = await session.scalar(
                    select(User).where(User.user_id == user.id)
                )
                data["locale"] = db_user.locale if db_user else "en"
                data["user_db"] = db_user
            else:
                data["locale"] = "en"
                data["user_db"] = None

            return await handler(event, data)
