from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Response:
    """Dataclass to transferitn ORM response."""

    id: UUID
    uploaded_image_id: str
    recognized_image_id: str
    generated_at: datetime | str
    objects: list["RecognizedObject"]  # type: ignore

    def get_labels(self) -> dict[str, int]:
        """Evaluate labels to dict with label: amount k-v."""
        return {obj.label: obj.amount for obj in self.objects}

    def __post_init__(self):
        if isinstance(self.generated_at, datetime):
            self.generated_at = self.generated_at.strftime("%d-%m-%Y %H:%M")
