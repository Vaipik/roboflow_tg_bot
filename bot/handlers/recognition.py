import logging

from aiogram import Bot, F, Router, html
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot.keyboards.recognition import uploaded_photo_inline_kb
from bot.keyboards.common import make_main_keyboard
from bot.states import UploadingPhotoForm

from bot.utils import RoboFlow

logger = logging.getLogger(__name__)

recognition_router = Router()


@recognition_router.message(F.text == "Generate new")
async def upload_image_command(message: Message, state: FSMContext):
    """
    This handler is for reply keyboard, and it is inital state for uploading photo.
    """
    await state.set_state(UploadingPhotoForm.waiting_upload)
    await message.answer(
        text=f"Upload a photo with {html.bold('lego')} after this message",
        reply_markup=ReplyKeyboardRemove()
    )


@recognition_router.callback_query(Text("cancel_response"))
async def upload_image_state(callback: CallbackQuery, state: FSMContext):
    """
    This handler is for inline keyboard, it makes opportunity to upload another photo.
    """
    await state.set_state(UploadingPhotoForm.waiting_upload)
    await callback.message.answer(text=f"Upload a photo with {html.bold('lego')} after this message", )
    await callback.answer()


@recognition_router.message(
    UploadingPhotoForm.waiting_upload,
    F.photo,
)
async def process_image(message: Message, state: FSMContext):
    """
    This handler is validataing that file is photo, updating user data by adding file_id in user data.
    Also gives possibility to choose another photo.
    """
    file_id = message.photo[-1].file_id  # file that was sent to the bot
    await message.reply(
        f"Okey, you have uploaded a photo.\n"
        f"If you want to continue, click {html.bold('Yes')}\n"
        f"if you want to upload another photo click {html.bold('No')}",
        reply_markup=uploaded_photo_inline_kb()
    )
    await state.update_data(file_id=file_id)
    await state.set_state(UploadingPhotoForm.answer)


@recognition_router.message(
    UploadingPhotoForm.waiting_upload
)
async def process_document_image(message: Message):
    """
    This handler is letting a user know that uploaded file is not photo
    """
    await message.answer(
        text="You need to upload compressed image"
    )


@recognition_router.callback_query(UploadingPhotoForm.answer, Text("make_response"))
async def generate_response(callback: CallbackQuery, state: FSMContext, bot: Bot, roboflow_api: RoboFlow):
    """
    Handler getting uploaded user photo into BytesIO,
    making request to roboflow api using photo in BytesIO and proceed it to the user via message
    """
    user_data = await state.get_data()
    file_id = user_data["file_id"]
    file = await bot.get_file(file_id)
    file_path = file.file_path
    image = await bot.download_file(file_path)
    response = await roboflow_api.recognize(image)

    # Following is just for testint
    # TODO: Rewrite when model will be ready
    await callback.message.answer(
        text=f"I have following answer according to your request:\n" + "\n".join(response),
        reply_markup=make_main_keyboard())
    await callback.answer(text="Redirecting to main menu", show_alert=True)
