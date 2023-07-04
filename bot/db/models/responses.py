import enum
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = UniqueConstraint("image_id", "model_id"),

    image_id: Mapped[str]
    chat_id: Mapped[int]
    recognized_image_id: Mapped[int]
    generated_at: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow)
    model_id: Mapped[UUID] = mapped_column(
        ForeignKey("neural_models.id")
    )
    objects: Mapped[list["Recognition"]] = relationship(  # type: ignore
        "Recognition", back_populates="response"
    )
    model: Mapped["NeuralModel"] = relationship(  # type: ignore
        "NeuralModel", back_populates="responses"
    )
