from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Recognition(Base):
    """This table is store object label and amount for the given response"""
    __tablename__ = "recognized_objects"
    label: Mapped[str]
    count: Mapped[int]
    response_id: Mapped[UUID] = mapped_column(
        ForeignKey("response.id")
    )
    response: Mapped["Response"] = relationship(  # type: ignore
        back_populates="objects"
    )


