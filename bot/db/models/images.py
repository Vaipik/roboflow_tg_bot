from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Image(Base):
    __tablename__ = "images"

    chat_image_id: Mapped[int]
    chat_id: Mapped[int]
    response: Mapped[list["Response"]] = relationship(
        back_populates="image", cascade="all, "
    )
