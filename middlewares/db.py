"""
Middleware for DB session injection and user locale resolution.
Each request gets its own session, locale, and user_db.
"""

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy import select

from database.engine import async_session_maker
from database.models import User
from i18n import t, resolve_ui_locale


class DbSessionMiddleware(BaseMiddleware):
    """
    Middleware that creates AsyncSession for each update
    and passes session, locale, and user_db into handler data.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            data["session"] = session

            # Resolve user_id from event
            user = data.get("event_from_user")
            if user:
                db_user = await session.scalar(
                    select(User).where(User.user_id == user.id)
                )
                data["locale"] = resolve_ui_locale(db_user.target_lang if db_user else "en")
                data["user_db"] = db_user
            else:
                data["locale"] = "en"
                data["user_db"] = None
            data["_"] = lambda key, **kwargs: t(data["locale"], key, **kwargs)

            return await handler(event, data)
