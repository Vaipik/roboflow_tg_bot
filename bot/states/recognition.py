from aiogram.fsm.state import State, StatesGroup


class UploadingPhotoForm(StatesGroup):
    """State for uploading handler."""

    waiting_upload = State()
    answer = State()
