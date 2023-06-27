import io

import aiohttp
import roboflow
from PIL import Image
from roboflow import Project

from bot.config import RoboFlowAPI


class RoboFlow:

    def __init__(self, project: Project):
        self.project = project
        self.__url = self.__make_url()

    def __make_url(self) -> str:
        project_name = self.project.name.replace(" ", "-").lower()

        url = f"https://api.roboflow.com/dataset/{project_name}/upload?api_key=API_KEY"  # TODO: Inject API_KEY
        return url

    def preprocess_image(self, image_content: io.BytesIO) -> Image.Image:
        image = Image.open(image_content).convert("RGB")

        return image

    def parse_response(self):
        pass

    async def recognize(self, image_content: io.BytesIO):
        image = self.preprocess_image(image_content)

        buffered = io.BytesIO()
        image.save(buffered, quality=90, format="JPEG")

        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("TELEGRAM2.jpg", buffered.getvalue(), content_type="image/jpeg")
            async with session.post(
                    url=self.__url,
                    data=data,
            ) as response:
                resp = await response.json()


def initialize_roboflow(settings: RoboFlowAPI) -> RoboFlow:
    project = roboflow.Roboflow(
        api_key=settings.private_key.get_secret_value()
    ). \
        workspace(). \
        project(settings.project_id.get_secret_value())

    roboflow_api = RoboFlow(project=project)
    return roboflow_api
