from sqlalchemy.orm import Mapped, relationship

from .base import Base


class NeuralModel(Base):
    __tablename__ = "neural_models"

    name: Mapped[str]
    version: Mapped[str]
    responses: Mapped[list["Response"]] = relationship(  # type: ignore
        "Response", back_populates="model"
    )
