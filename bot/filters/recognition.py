from uuid import UUID

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.infrastructure.db.uow import SQLAlchemyUoW


class CheckImageFilter(BaseFilter):
    """Check previous user response."""

    async def __call__(
        self, callback: CallbackQuery, state: FSMContext, uow: SQLAlchemyUoW
    ) -> dict[str, UUID] | bool:
        """Check image with file_unique_id for previous response."""
        user_data = await state.get_data()
        file_unique_id = user_data["file_unique_id"]
        chat_id = user_data["chat_id"]

        checked_image_id = await uow.uploaded_images.check_image(
            file_unique_id, chat_id
        )
        if checked_image_id:
            return {"checked_image_id": checked_image_id}

        return False
