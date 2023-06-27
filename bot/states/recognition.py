from aiogram.fsm.state import State, StatesGroup


class UploadingPhotoForm(StatesGroup):
    waiting_upload = State()
    answer = State()
