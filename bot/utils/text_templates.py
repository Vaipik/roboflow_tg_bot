from aiogram import html

from bot.keyboards.recognition import RecognitionKeyboardButtons


def roboflow_success_response(labels: dict[str, int]) -> str:
    """
    Generate string with key: value pairs separated by newline symbol.

    :param labels: a dict with labels and their amount at image.
    :return: formatted string.
    """
    result = "I have following answer according to your request:\n" + "\n".join(
        [
            f"Label <b>{label}</b>: met <b>{amount}</b> times"
            for label, amount in labels.items()
        ]
    )
    return result


def new_upload_photo_text() -> str:
    """Text displayed when user click on Generate New or choose another upload."""
    return f"Upload a photo with {html.bold('lego')} after this message"


def uploaded_photo_text(buttons: RecognitionKeyboardButtons) -> str:
    """Text displayed when user will sucessfully upload a photo."""
    string = f"""Okey, you have uploaded a photo.\n
    If you want to continue, click {html.bold(buttons.make_response)}\n
    if you want to upload another photo click {html.bold(buttons.upload_another)}"""
    return string
