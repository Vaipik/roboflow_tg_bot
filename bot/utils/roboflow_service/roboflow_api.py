import io
import logging
from pathlib import Path
from typing import Any

import roboflow
from roboflow.models.object_detection import ObjectDetectionModel

from PIL import Image, ImageDraw, ImageFont
from bot.config import NeuralNetwork, RoboFlowAPI


logger = logging.getLogger(__name__)


class RoboFlow:
    """Operate with roboflow API using roboflow package."""

    def __init__(self, model: ObjectDetectionModel, bot_token: str, font_path: Path):
        """
        Initialize roboflow service.

        :param model: current roboflow model for project and version.
        :param bot_token: required for uploading user photo to robofolow.
        """
        self.model = model
        self.bot_token = bot_token
        self.font_path = font_path

    def make_url(self, file_path) -> str:
        """Make url which allow image being sent to roboflow."""
        return f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"

    def parse_response(
        self, draw: ImageDraw.ImageDraw, response: list[dict[str, Any]]
    ) -> dict[str, int | float]:
        """
        Parse response from roboflow and draw boundary boxes on image.

        Example of roboflow response
        {
            "predictions": [
                {
                    "x": 662.0,  - center of the object X axis
                    "y": 452.0, - center of the object Y axis
                    "width": 184.0, - width of rectangle with center in X, Y
                    "height": 154.0, - height of rectange wih center in X,Y
                    "confidence": 0.6081843972206116, probability
                    "class": "className",  - detected class
                    "image_path": "path",  - image path or url
                    "prediction_type": "ObjectDetectionModel"
                }
            ]
        }.
        """
        result: dict[str, float] = {}
        with open(self.font_path, "rb") as f:
            font = ImageFont.truetype(font=f, size=14)

        for prediction in sorted(response, key=lambda x: (len(x["class"]), x["class"])):
            label = prediction["class"]
            confidence = prediction["confidence"] * 100  # convert to %
            result[label] = result.get(label, 0) + 1

            x1 = prediction["x"] - prediction["width"] / 2
            x2 = prediction["x"] + prediction["width"] / 2
            y1 = prediction["y"] - prediction["height"] / 2
            y2 = prediction["y"] + prediction["height"] / 2

            draw.rectangle(((x1, y1), (x2, y2)), fill=(25, 25, 112, 140))
            draw.rectangle(((x1, y1), (x2, y2)), outline=(225, 225, 0, 255), width=3)
            draw.text(
                (x1 + 5, y1 - 15),
                text=f"{label} - {confidence:.2f}%",
                fill="yellow",
                font=font,
            )
        return result

    def recognize(
        self, file_bytes: io.BytesIO, file_path: str
    ) -> tuple[dict, bytes] | None:
        """Make prediction using roboflow API. Returns response with boundary boxes."""
        url = self.make_url(file_path)
        try:
            response: dict[str, list[dict]] | None = self.model.predict(
                url, hosted=True
            ).json()
        except Exception as e:
            logger.error(e)
        else:
            predictions = response.get("predictions")
            if predictions:
                img = Image.open(file_bytes)
                draw = ImageDraw.Draw(img, "RGBA")
                result = self.parse_response(draw, predictions)

                # Saving image to bytes
                img_to_bytes = io.BytesIO()
                img.save(img_to_bytes, format=img.format)
                img_bytes = img_to_bytes.getvalue()

                return result, img_bytes

        return None


def initialize_roboflow(
    *, roboflow_api_settings: RoboFlowAPI, neural_network: NeuralNetwork, bot_token: str
) -> RoboFlow:
    """Initialize roboflow service with roboflow roboflow_api_settings."""
    FONT_DIR = Path(__file__).parent
    model = (
        roboflow.Roboflow(api_key=roboflow_api_settings.private_key.get_secret_value())
        .workspace()
        .project(roboflow_api_settings.project_id.get_secret_value())
        .version(neural_network.version.replace("v", ""))
        .model
    )
    roboflow_api = RoboFlow(
        model=model, bot_token=bot_token, font_path=FONT_DIR / "FreeMonospacedBold.ttf"
    )
    return roboflow_api
