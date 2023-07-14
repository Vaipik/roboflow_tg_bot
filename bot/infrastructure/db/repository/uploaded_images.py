from uuid import UUID

from sqlalchemy import select

from .base import SQLAlchemyRepository
from bot.infrastructure.db.models import UploadedImage


class UploadedImageRepository(SQLAlchemyRepository):
    """Is used to perform operations with files sent by user."""

    async def save_image(self, file_id: str, file_unique_id: str, chat_id: int) -> UUID:
        """
        Save imaga sent by user.

        :param file_id: image id that can be used for downloading. Not unique for
        file_unique_id.
        :param file_unique_id: unique image id
        :param chat_id: chat id in which file was sent.
        :return: ORM entity with UploadedImage.
        """
        new_image = UploadedImage(
            file_id=file_id, file_unique_id=file_unique_id, chat_id=chat_id
        )
        self.session.add(new_image)
        await self.session.flush([new_image])
        pk = new_image.id
        return pk

    async def check_image(self, file_unique_id: str, chat_id: int) -> UUID | None:
        """
        Check was image sent previously or not.

        :param file_unique_id: unique identifier that will be checked
        :param chat_id: chat id in which file was sent
        :return: Primary key of image or None.
        """
        stmt = select(UploadedImage.id).where(
            UploadedImage.file_unique_id == file_unique_id,
            UploadedImage.chat_id == chat_id,
        )
        result = await self.session.scalar(stmt)
        return result
