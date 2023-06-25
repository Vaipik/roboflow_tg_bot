import io

import requests
import roboflow
from PIL import Image
from requests_toolbelt import MultipartEncoder
from roboflow import Project

from bot.config import cfg

project = roboflow.Roboflow(
    api_key=cfg.roboflow.private_key.get_secret_value()
). \
    workspace(). \
    project(cfg.roboflow.project_id.get_secret_value())


class RoboFlow:

    def __init__(self, project: Project):
        self.project = project

    def preprocess_image(self, image_content: bytes) -> Image.Image:
        image = Image.open(image_content).convert("RGB")

        return image

    def parse_response(self):
        pass

    def recognize(self, image_content: bytes):
        image = self.preprocess_image(image_content)

        # Following was taken from the roboflow docs
        buffered = io.BytesIO()
        image.save(buffered, quality=90, format="JPEG")

        # Construct the Upload URL
        url = f"https://api.roboflow.com/dataset/{cfg.roboflow.project_name.get_secret_value()}/upload?api_key={cfg.roboflow.private_key.get_secret_value()}"
        print(url)
        data = MultipartEncoder(fields={'file': (
            "TELEGRAM.jpg",
            buffered.getvalue(), "image/jpeg")})

        response = requests.post(url, data=data, headers={'Content-Type': data.content_type})

        print(response.json())


roboflow_api = RoboFlow(project=project)
