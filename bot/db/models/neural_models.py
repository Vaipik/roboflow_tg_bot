from sqlalchemy.orm import Mapped, relationship

from .base import Base


class NeuralModel(Base):
    """
    Store information about NN.\n
    name: str name of NN.\n
    version: str version of NN.\n
    """

    __tablename__ = "neural_models"

    name: Mapped[str]
    version: Mapped[str]
    responses: Mapped[list["Response"]] = relationship(  # type: ignore
        back_populates="model"
    )

    def __repr__(self):
        return f"[NN {self.name}v{self.version}]"
