import logging
from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.infrastructure.db.repository import ResponseRepository, UploadedImageRepository


logger = logging.getLogger(__name__)


class SQLAlchemyBaseUoW:
    """Base implementation of Unit of Work pattern."""

    def __init__(self, session: AsyncSession):
        """Initialize UoW with session."""
        self.session = session

    async def commit(self) -> None:
        """Commit whole transaction."""
        try:
            await self.session.commit()
        except IntegrityError as e:
            logger.error(e)

    async def rollback(self) -> None:
        """Rollback transaction."""
        await self.session.rollback()


class SQLAlchemyUoW(SQLAlchemyBaseUoW):
    """Implementation UoW with repositories."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        responses_repo: Type[ResponseRepository],
        uploaded_images_repo: Type[UploadedImageRepository],
    ):
        """Initialize UoW with db operations."""
        self.responses = responses_repo(session)
        self.uploaded_images = uploaded_images_repo(session)
        super().__init__(session)
