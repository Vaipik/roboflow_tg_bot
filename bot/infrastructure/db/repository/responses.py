from uuid import UUID

from sqlalchemy import select, func, desc
from sqlalchemy.orm import joinedload

from bot import dto
from bot.infrastructure.db.models import (
    RecognizedObject,
    Response,
    UploadedImage,
    NeuralModel,
)
from .base import SQLAlchemyRepository


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

    async def get_response_by_uploaded_image_id(
        self, uploaded_image_id: UUID, model: NeuralModel
    ) -> dto.Response:
        """Return DTO for response table model."""
        return (
            await self._get_response_by_uploaded_image_id(uploaded_image_id, model)
        ).to_dto()  # type: ignore[return-value]

    async def _get_response_by_uploaded_image_id(
        self, uploaded_image_id: UUID, model: NeuralModel
    ) -> Response | None:
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

        result = await self.session.scalar(stmt)
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
        if response.response_image_id:
            [
                RecognizedObject(label=label, amount=amount, response=response)
                for label, amount in objects.items()
            ]
        self.session.add(response)

    async def get_user_responses(
        self, chat_id: int, offset: int = 0, limit: int = 6
    ) -> list[dto.ShortenResponse] | None:
        """Return list of user respones in dto.Response or None."""
        result = await self._get_user_responses(chat_id, offset, limit)
        if result:
            return [row.to_dto(shorten=True) for row in result]

        return None

    async def _get_user_responses(self, chat_id: int, offset: int = 0, limit: int = 6):
        """
        User responses with offset and limit. Default offset is 0 and limit is 6.

        :param chat_id: user identifier.
        :param offset: how much should be skipped. Used for pagination.
        :param limit:  how much should be returned. Used for pagination.
        :return:
        """
        stmt = (
            select(Response)
            .join(Response.uploaded_image)
            .where(
                UploadedImage.chat_id == chat_id,
                Response.response_image_id.is_not(None),
            )
            .order_by(desc(Response.generated_at))
            .offset(offset)
            .limit(limit)
        )
        response = await self.session.scalars(stmt)
        result = response.unique().all()
        return result

    async def count_responses(self, chat_id: int) -> int | None:
        """
        Count amount of user responses.

        :param chat_id: chat identtifier
        :return: total amount of chat(user) responses or None.
        """
        stmt = (
            select(func.count(Response.id))
            .join(Response.uploaded_image)
            .where(UploadedImage.chat_id == chat_id)
        )
        response = await self.session.execute(stmt)
        return response.scalar_one_or_none()

    async def get_user_response_by_id(self, response_id: UUID | str) -> dto.Response:
        """Get response from db and converts it do dto.Response."""
        response = await self._get_user_response_by_id(response_id)
        return response.to_dto()  # type: ignore[return-value]

    async def _get_user_response_by_id(
        self, response_id: UUID | str
    ) -> Response | None:
        stmt = (
            select(Response)
            .where(Response.id == response_id)
            .options(joinedload(Response.objects, innerjoin=True))
        )

        result = await self.session.scalar(stmt)
        return result


"""
SELECT r.response_image_id, r.generated_at, r.id FROM responses r
    JOIN uploaded_images u ON r.uploaded_image_id = u.id
WHERE u.chat_id = chat_id
ORDER BY r.generated_at DESC
OFFSET 0
LIMIT 6;
"""
