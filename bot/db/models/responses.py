import enum
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ModelType(str, enum.Enum):
    YOLOv8 = "YOLOv8"
    YOLOv5 = "YOLOv5"


class Response(Base):
    recognized_image_id: Mapped[int]
    generated_at: Mapped[datetime] = mapped_column()
    model: Mapped[ModelType]
    version: Mapped[str]
    chat_image_id: Mapped[UUID] = mapped_column(
        ForeignKey("images.id")
    )
    image: Mapped["Image"] = relationship(  # type: ignore
        "Image", back_populates="response"
    )
    objects: Mapped[list["Recognition"]] = relationship(  # type: ignore
        "Recognition", back_populates="response"
    )
