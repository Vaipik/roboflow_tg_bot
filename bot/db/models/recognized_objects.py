from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class RecognizedObject(Base):
    """
    This table is store object label and amount for the given response.\n
    label: str - label of object.\n
    amount: int - quantity of objects per response.\n
    response_id: FK[UUID] - FK to response.
    """

    __tablename__ = "recognized_objects"
    label: Mapped[str]
    amount: Mapped[int]
    response_id: Mapped[UUID] = mapped_column(ForeignKey("responses.id"))
    response: Mapped["Response"] = relationship(  # type: ignore
        back_populates="objects"
    )

    def __repr__(self):
        return f"[RO {self.label}={self.amount}]"
