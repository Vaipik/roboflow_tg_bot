from sqlalchemy import select

from .base import SQLAlchemyRepository
from bot.db.models import NeuralModel


class NeuralModelRepository(SQLAlchemyRepository):
    """For operating with NeuralModel entity."""

    async def insert_on_startup(self, name: str, version: str) -> NeuralModel:
        """
        Insert data about neural network model.

        :param name: model name.
        :param version: model version.
        :return: ORM instance of neural model.
        """
        model = NeuralModel(name=name, version=version)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def check_on_startup(self, name: str, version: str) -> NeuralModel | None:
        """
        Check if actual model in db.

        :param name: model name.
        :param version: model version.
        :return: ORM instance of neural model if exists.
        """
        stmt = select(NeuralModel).where(
            NeuralModel.name == name,
            NeuralModel.version == version,
        )
        result = await self.session.scalar(stmt)
        return result
