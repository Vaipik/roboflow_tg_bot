from sqlalchemy.orm import Mapped, relationship

from .base import Base


class NeuralModel(Base):
    """
    Store information about NN.

    name: str name of NN.
    version: str version of NN.
    """

    __tablename__ = "neural_models"

    name: Mapped[str]
    version: Mapped[str]
    responses: Mapped[list["Response"]] = relationship(  # type: ignore
        back_populates="model"
    )

    def __repr__(self) -> str:
        return f"[NN {self.name}v{self.version}]"
