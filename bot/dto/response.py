from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Response:
    """Dataclass to transferitn ORM response."""

    uploaded_image_id: str
    recognized_image_id: str
    generated_at: datetime
    objects: list["RecognizedObject"]  # type: ignore
    model: "NeuralModel"  # type: ignore

    def get_labels(self) -> dict[str, int]:
        """Evaluate labels to dict with label: amount k-v."""
        return {obj.label: obj.amount for obj in self.objects}
