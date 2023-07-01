import io
import logging
from typing import Optional

import roboflow  # type: ignore

from PIL import Image, ImageDraw
from bot.config import RoboFlowAPI

logger = logging.getLogger(__name__)


class RoboFlow:
    """Class that operates with roboflow api via uploading photo to roboflow and parsing response"""

    def __init__(self, model, bot_token: str):
        self.model = model
        self.bot_token = bot_token

    def make_url(self, file_path):
        return f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"

    def make_img(self):
        pass

    def parse_response(self, draw: ImageDraw.ImageDraw, response: dict[str, list[dict]]) -> dict:
        """
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
        }
        """

        result: dict[str, float] = {}
        for prediction in response["predictions"]:
            class_ = prediction["class"]
            confidence = prediction["confidence"] * 100  # convert to %
            result[class_] = result.get(class_, 0) + 1
            x1 = prediction["x"] - prediction["width"] / 2
            x2 = prediction["x"] + prediction["width"] / 2
            y1 = prediction["y"] - prediction["height"] / 2
            y2 = prediction["y"] + prediction["height"] / 2
            draw.rectangle((x1, y1, x2, y2), outline="darkorange")
            draw.text((x1, y1), text=f"{class_} - {confidence:.2f}%", fill="darkorange")
        return result

    async def recognize(self, file_bytes: io.BytesIO, file_path: str) -> Optional[tuple[dict, bytes]]:
        url = self.make_url(file_path)
        response: Optional[dict[str, list[dict]]] = self.model.predict(url, hosted=True).json()
        if response:
            img = Image.open(file_bytes)
            draw = ImageDraw.Draw(img)
            result = self.parse_response(draw, response)
            # Saving image to bytes
            img_to_bytes = io.BytesIO()
            img.save(img_to_bytes, format=img.format)
            img_bytes = img_to_bytes.getvalue()

            return result, img_bytes

        return None
def initialize_roboflow(settings: RoboFlowAPI, bot_token: str) -> RoboFlow:
    model = roboflow.Roboflow(
        api_key=settings.private_key.get_secret_value()
    ). \
        workspace(). \
        project(settings.project_id.get_secret_value()). \
        version(2).model

    roboflow_api = RoboFlow(model, bot_token)
    return roboflow_api
