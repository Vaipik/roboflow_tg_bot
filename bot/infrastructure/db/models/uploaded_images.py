from sqlalchemy.orm import Mapped, relationship

from .base import Base


class UploadedImage(Base):
    """Stores user uploaded files."""

    __tablename__ = "uploaded_images"

    file_unique_id: Mapped[str]
    file_id: Mapped[str]
    chat_id: Mapped[int]
    response: Mapped[list["Response"]] = relationship(  # type: ignore
        back_populates="uploaded_image", cascade="all, delete-orphan"
    )
