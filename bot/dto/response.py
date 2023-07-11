from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    """Dataclass to transferitn ORM response."""

    recognized_image_id: str
    objects: list["RecognizedObject"]  # type: ignore

    def get_labels(self) -> dict[str, int]:
        """Evaluate labels to dict with label: amount k-v."""
        return {obj.label: obj.amount for obj in self.objects}
