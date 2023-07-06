from sqlalchemy.orm import Mapped, relationship

from .base import Base


class UploadedImage(Base):
    """
    Stores user uploaded files.\n
    file_unique_id: str is used to identify was file uploaded previously.\n
    file_id: str is used to make possibility download this file again.\n
    chat_id: int is used to link user with image
    """

    __tablename__ = "uploaded_images"

    file_unique_id: Mapped[str]
    file_id: Mapped[str]
    chat_id: Mapped[int]
    response: Mapped[list["Response"]] = relationship(  # type: ignore
        back_populates="uploaded_image"
    )
