import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from bot import dto
from bot.infrastructure.db.models import (
    RecognizedObject,
    Response,
    UploadedImage,
    NeuralModel,
)
from .base import SQLAlchemyRepository


logger = logging.getLogger(__name__)


class ResponseRepository(SQLAlchemyRepository):
    """Main repository for operating with responses."""

    async def check_user_image(self, file_unique_id: str, chat_id: int) -> UUID | None:
        """
        Did user previously upload image to telegram.

        :param: file_unique_id: file id that should be checked for response.
        :param: chat_id: chat id where this file was sent.
        :return: True if photo was uploaded, False if it wasn't.
        """
        statement = (
            select(Response.uploaded_image_id)
            .join(Response.uploaded_image)
            .where(
                UploadedImage.file_unique_id == file_unique_id,
                UploadedImage.chat_id == chat_id,
            )
        )
        response = await self.session.scalar(statement)
        return response

    async def check_user_response(
        self, uploaded_image_id: str, model: NeuralModel
    ) -> bool:
        """
        Was user request successful or not.

        :param uploaded_image_id: the image id to be checked
        :param model: instance of NN for which request was performed
        :return: True if response was successful False it wasn't.
        """
        statement = select(Response.response_image_id).where(
            Response.uploaded_image_id == uploaded_image_id, Response.model == model
        )
        response = await self.session.scalars(statement)
        return True if response else False

    async def get_user_response(
        self, uploaded_image_id: UUID, model: NeuralModel
    ) -> dto.Response:
        """
        Return user response with recognized objects for given image_id.

        :param uploaded_image_id: image id for which NN made recognizing
        :param model: instance of NN for which performed recognizing
        :return: Response instance.
        """
        stmt = (
            select(Response)
            .where(
                Response.uploaded_image_id == uploaded_image_id, Response.model == model
            )
            .options(joinedload(Response.objects, innerjoin=True))
        )

        response = await self.session.scalar(stmt)
        logger.error(response)
        result = dto.Response(
            recognized_image_id=response.response_image_id, objects=response.objects
        )
        return result

    async def save_response(
        self,
        uploaded_image_id: UUID,
        model: NeuralModel,
        objects: dict[str, int] | None = None,
        recognized_image_id: str | None = None,
    ) -> None:
        """
        Save generated response to db.

        :param uploaded_image_id: image id for which NN made recognizing
        :param model: instance of NN for which performed recognizing
        :param objects: objects dict with {label: amount}
        :param recognized_image_id: image id with boundary boxes for recognized objects
        :return: None.
        """
        response = Response(
            uploaded_image_id=uploaded_image_id,
            model=model,
            response_image_id=recognized_image_id,
        )
        [
            RecognizedObject(label=label, amount=amount, response=response)
            for label, amount in objects.items()
        ]
        self.session.add(response)
