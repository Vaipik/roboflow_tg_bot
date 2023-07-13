from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot import dto
from .base import Base


class Response(Base):
    """
    Stores response from neural network.

    response_image_id: str | None file id for downloading if recognize was succesful.
    generated_at: datetime when response was made.
    uploaded_image_id: FK[UUID] image which should be recognized.
    model_id: FK[UUID] NN model which was used for recognition.
    """

    __tablename__ = "responses"
    __table_args__ = (
        UniqueConstraint("response_image_id", "uploaded_image_id", "model_id"),
    )

    response_image_id: Mapped[str | None]
    generated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    # FK
    uploaded_image_id: Mapped[UUID] = mapped_column(ForeignKey("uploaded_images.id"))
    model_id: Mapped[UUID] = mapped_column(ForeignKey("neural_models.id"))
    # Alchemy relationships
    objects: Mapped[list["RecognizedObject"]] = relationship(  # type: ignore
        back_populates="response"
    )
    uploaded_image: Mapped["UploadedImage"] = relationship(  # type: ignore
        back_populates="response", uselist=False
    )
    model: Mapped["NeuralModel"] = relationship(  # type: ignore
        back_populates="responses", uselist=False
    )

    def __repr__(self) -> str:
        return f"[R {self.response_image_id=} | {self.uploaded_image_id}]"

    def to_dto(self) -> dto.Response:
        """Convert to dto."""
        return dto.Response(
            id=self.id,
            uploaded_image_id=self.uploaded_image_id,
            recognized_image_id=self.response_image_id,
            generated_at=self.generated_at,
            objects=self.objects,
        )
