from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    recognized_image_id: str
    labels: list[str]
    amount: list[int]
