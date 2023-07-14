from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ShortenResponse:
    """Shorter version of response. Used for paginator."""

    id: UUID
    generated_at: datetime | str

    def __post_init__(self):
        if isinstance(self.generated_at, datetime):
            self.generated_at = self.generated_at.strftime("%d-%m-%Y %H:%M")


@dataclass
class Response(ShortenResponse):
    """Dataclass to transferitn ORM response."""

    uploaded_image_id: str
    recognized_image_id: str | None
    objects: list["RecognizedObject"] | None  # type: ignore

    def get_labels(self) -> dict[str, int]:
        """Evaluate labels to dict with label: amount k-v."""
        return {obj.label: obj.amount for obj in self.objects}
