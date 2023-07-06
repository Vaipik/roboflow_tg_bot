from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .neural_models import NeuralModel
    from .recognition import Recognition


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = (UniqueConstraint("image_id", "model_id"),)

    image_id: Mapped[str]
    chat_id: Mapped[int]
    recognized_image_id: Mapped[str]
    generated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    model_id: Mapped[UUID] = mapped_column(ForeignKey("neural_models.id"))
    objects: Mapped[list[Recognition]] = relationship(
        "Recognition", back_populates="response"
    )
    model: Mapped[NeuralModel] = relationship("NeuralModel", back_populates="responses")
