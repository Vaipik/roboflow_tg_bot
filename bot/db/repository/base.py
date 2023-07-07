from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    """Base class with db session."""

    def __init__(self, session: AsyncSession):
        self.session = session
