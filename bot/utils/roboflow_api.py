import logging
import roboflow


from bot.config import RoboFlowAPI


logger = logging.getLogger(__name__)


class RoboFlow:

    def __init__(self, model, bot_token: str):
        self.model = model
        self.bot_token = bot_token

    def make_url(self, file_path):
        return f"https://api.telegram.org/file/bot{self.bot_token}/{file_path}"

    def make_img(self):
        pass

    def parse_response(self, response: dict[list[dict]]) -> list[str]:
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
        result = []
        for prediction in response["predictions"]:
            class_ = prediction["class"]
            confidence = prediction["confidence"] * 100
            result.append(f"class <b>{class_}</b> with confidence - <b>{confidence:.2f}</b>")

        return result

    async def recognize(self, file_path: str) -> list[str]:
        # return self.parse_response()
        url = self.make_url(file_path)
        response = self.model.predict(url, hosted=True).json()

        return self.parse_response(response)


def initialize_roboflow(settings: RoboFlowAPI, bot_token: str) -> RoboFlow:
    model = roboflow.Roboflow(
        api_key=settings.private_key.get_secret_value()
    ). \
        workspace(). \
        project(settings.project_id.get_secret_value()). \
        version(2).model

    roboflow_api = RoboFlow(model, bot_token)
    return roboflow_api
