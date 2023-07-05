import logging

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot import dto
from bot.db.models import Response
from .base import SQLAlchemyRepository

logger = logging.getLogger(__name__)


class ResponseRepository(SQLAlchemyRepository):

    async def check_user_image(self, image_id: str, chat_id: int) -> bool:
        """
        Did user previously upload image to telegram
        :return: True if photo was uploaded, False if it wasn't
        """
        statement = select(Response).where(Response.image_id == image_id, Response.chat_id == chat_id)
        result = await self.session.scalar(statement)
        logger.info(result)
        return True if result else False

    async def get_user_response(self, image_id: str, chat_id: int) -> dto.Response:
        """

        :param image_id:
        :param chat_id:
        :return:
        """
        statement = select(Response). \
            options(joinedload(Response.objects, innerjoin=True)). \
            where(Response.image_id == image_id, Response.chat_id == chat_id)
        response = await self.session.scalars(statement)

    async def save_user_image(self, image_id: str, chat_id: int) -> Response:
        """
        Saving user uploaded image into db
        :param image_id: image_id given by tg from their server
        :param chat_id: chat id where this image was uploaded
        :return: None
        """
        uploaded_image = Response(
            image_id=image_id,
            chat_id=chat_id
        )
        self.session.add(uploaded_image)
        await self.session.flush()
        await self.session.refresh(uploaded_image)
        return uploaded_image
