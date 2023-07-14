from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RecognizedObject(Base):
    """
    This table is store object label and amount for the given response.

    label: str - label of object.
    amount: int - quantity of objects per response.
    response_id: FK[UUID] - FK to response.
    """

    __tablename__ = "recognized_objects"
    label: Mapped[str]
    amount: Mapped[int]
    response_id: Mapped[UUID] = mapped_column(
        ForeignKey("responses.id", ondelete="CASCADE")
    )
    response: Mapped["Response"] = relationship(  # type: ignore
        back_populates="objects", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"[RO {self.label}={self.amount}]"
