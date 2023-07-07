from dataclasses import dataclass

from bot.db import models


@dataclass(frozen=True)
class Response:
    """Dataclass to transferitn ORM response."""

    recognized_image_id: str
    objects: list[models.RecognizedObject]

    def get_labels(self) -> dict[str, int]:
        """Evaluate labels to dict with label: amount k-v."""
        return {obj.label: obj.amount for obj in self.objects}
