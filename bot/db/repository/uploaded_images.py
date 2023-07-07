import logging

from sqlalchemy import select

from .base import SQLAlchemyRepository
from bot.db.models import UploadedImage


logger = logging.getLogger(__name__)


class UploadedImageRepository(SQLAlchemyRepository):
    """Is used to perform operations with files sent by user."""

    async def save_image(
        self, file_id: str, file_unique_id: str, chat_id: int
    ) -> UploadedImage:
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
        await self.session.commit()
        await self.session.refresh(new_image)
        return new_image

    async def check_image(
        self, file_unique_id: str, chat_id: int
    ) -> UploadedImage | None:
        """
        Check was image sent previously or not.

        :param file_unique_id: unique identifier that will be checked
        :param chat_id: chat id in which file was sent
        :return: ORM instance if it exists otherwise None.
        """
        stmt = select(UploadedImage).where(
            UploadedImage.file_unique_id == file_unique_id,
            UploadedImage.chat_id == chat_id,
        )
        result = await self.session.scalar(stmt)
        logger.info(f"\n\n\n{result}\n\n\n")
        return result
