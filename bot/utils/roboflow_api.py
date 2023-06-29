import io
import logging
import roboflow

from PIL import Image, ImageDraw
from bot.config import RoboFlowAPI

logger = logging.getLogger(__name__)

ex = {
    'predictions': [
        {
            'x': 507.0,
            'y': 120.5,
            'width': 210.0,
            'height': 185.0,
            'confidence': 0.9804140329360962,
            'class': '4672',
        },
        {
            'x': 700.0,
            'y': 318.0,
            'width': 98.0,
            'height': 128.0,
            'confidence': 0.9740188121795654,
            'class': '65084',
        },
        {
            'x': 591.0,
            'y': 232.5,
            'width': 78.0,
            'height': 83.0,
            'confidence': 0.958608865737915,
            'class': '76371',
        },
        {
            'x': 420.5,
            'y': 215.0,
            'width': 83.0,
            'height': 88.0,
            'confidence': 0.9552126526832581,
            'class': '3437',
        },
        {
            'x': 632.5,
            'y': 101.5,
            'width': 81.0,
            'height': 67.0,
            'confidence': 0.95378577709198,
            'class': '51409',
        },
        {
            'x': 223.0,
            'y': 137.5,
            'width': 260.0,
            'height': 147.0,
            'confidence': 0.949457049369812,
            'class': '51704',
        },
        {
            'x': 460.5,
            'y': 348.0,
            'width': 79.0,
            'height': 78.0,
            'confidence': 0.9466232061386108,
            'class': '51409'
        },
        {
            'x': 309.5,
            'y': 341.0,
            'width': 77.0,
            'height': 82.0,
            'confidence': 0.9431760907173157,
            'class': '3437',
        },
        {
            'x': 622.0,
            'y': 416.5,
            'width': 88.0,
            'height': 83.0,
            'confidence': 0.8960342407226562,
            'class': '3437',
        },
        {
            'x': 383.0,
            'y': 405.0,
            'width': 130.0,
            'height': 100.0,
            'confidence': 0.8937169313430786,
            'class': '40666',
        },
        {
            'x': 292.5,
            'y': 509.5,
            'width': 123.0,
            'height': 147.0,
            'confidence': 0.8924219608306885,
            'class': '3011',
        },
        {
            'x': 569.5,
            'y': 365.5,
            'width': 97.0,
            'height': 107.0,
            'confidence': 0.8219860792160034,
            'class': '98223',
        },
        {
            'x': 244.0,
            'y': 340.0,
            'width': 78.0,
            'height': 80.0,
            'confidence': 0.6300634145736694,
            'class': '98223',
        },
        {
            'x': 570.0,
            'y': 365.0,
            'width': 98.0,
            'height': 108.0,
            'confidence': 0.5922647714614868,
            'class': '98252',
        },
    ]
}


class RoboFlow:
    """Class that operates with roboflow api via uploading photo to roboflow and parsing response"""

    def __init__(self, model, bot_token: str):
        self.model = model
        self.bot_token = bot_token

    def make_url(self, file_path):
        return f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"

    def make_img(self):
        pass

    def parse_response(self, draw: ImageDraw.ImageDraw, response: dict[list[dict]] = ex) -> dict:
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

        result = {}
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

    async def recognize(self, file_bytes: io.BytesIO, file_path: str) -> tuple[dict, bytes]:
        url = self.make_url(file_path)
        response = self.model.predict(url, hosted=True).json()

        img = Image.open(file_bytes)
        draw = ImageDraw.Draw(img)
        result = self.parse_response(draw, response)
        # Saving image to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=img.format)
        img_bytes = img_bytes.getvalue()

        return result, img_bytes


def initialize_roboflow(settings: RoboFlowAPI, bot_token: str) -> RoboFlow:
    model = roboflow.Roboflow(
        api_key=settings.private_key.get_secret_value()
    ). \
        workspace(). \
        project(settings.project_id.get_secret_value()). \
        version(2).model

    roboflow_api = RoboFlow(model, bot_token)
    return roboflow_api
