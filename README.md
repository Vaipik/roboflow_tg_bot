RoboflowBot: Telegram bot that recognize lego items for given image.
===
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ruff](https://github.com/Vaipik/roboflow_tg_bot/actions/workflows/test.yaml/badge.svg)](https://github.com/Vaipik/roboflow_tg_bot/actions/workflows/test.yaml)
___
This telegram bot will try to recognize lego items on the photo that user uploads to it.
Start page of this bot looks like:
<img src="readme/start_page.png"/>
After clicking <b>start</b> button user are able to choose two following options by using keyboard:
<img src="readme/start_main_menu.png"/>
If user will click on <b>Previoues results</b> and user didn't make any request to bot,
the last one will make a response with following text and main keyboard will be still available.
<img src="readme/no_previous_result.png"/>
To perform a prediction users must click on <b>Generate new</b> button.
~~User can send a message with this text and it will also work fine.~~
Afterwards bot will propose to download a **PHOTO**, not a **DOCUMENT**
<img src="readme/uploaded_photo.png"/>
If user will send not a photo bot will make a following answer:
<img src="readme/not_photo.png"/>
After downloading a photo user will be asked to confirm upload or to upload another photo
by using inline keyborad
<img src="readme/confirmation.png"/>
In case user clicks **No** bot will propose upload another photo
<img src="readme/clicked_no_on_inline_kb.png"/>
Otherwise it will try to make a prediction. Case for success prediction:
<img src="readme/recognize_photo.png"/>
Recognized **lego items** with boundary boxes and **lego item number** with probability
at the of boundary boxes are shown. This success response will be used in **previous results**.
If neural network is not able to recognize anything it will respond as following:
<img src="readme/unsuccess_example.png"/>
After response bot will redirect user to main menu.
If user will have a successfull response **previous results** menu will be available.
It shows 6 responses per page separated into 3 rows with 2 columns.
It displays repsonses via inline keyboard functionality.
Each response marked in following way: _**dd-mm-yyyy HH-MM**_.
To obtain previoues response user must just click on the desired data.
First page of responses:
<img src="readme/responses_first_page.png"/>
The last page of responses:
<img src="readme/responses_last_page.png"/>
___
### Environment variables
To start this project you need define following environment variables. They are also present in .env.example
```
BOT_TOKEN=bot_token
ROBOFLOWAPI__PRIVATE_KEY=roboflow_api_private_key
ROBOFLOWAPI__PUBLISHABLE_KEY=roboflow_api_publishable_key
ROBOFLOWAPI__PROJECT_ID=roboflow_project_id
NN__NAME=neural_network_name
NN__VERSION=neural_network_version
DB__HOST=host
DB__PORT=port
DB__NAME=database_name
DB__USER=user
DB__PASSWORD=password
```
