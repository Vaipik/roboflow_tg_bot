from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .responses import Response


class NeuralModel(Base):
    __tablename__ = "neural_models"

    name: Mapped[str]
    version: Mapped[str]
    responses: Mapped[list[Response]] = relationship("Response", back_populates="model")

    def __repr__(self):
        return f"[NN {self.name}v{self.version}]"
