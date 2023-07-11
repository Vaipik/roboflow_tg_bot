import asyncio
import logging
from uuid import UUID

from aiogram import Bot, F, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile

from bot.filters.recognition import CheckImageFilter
from bot.keyboards.common import make_main_keyboard, CommonKeyBoardButtons
from bot.keyboards.recognition import (
    uploaded_photo_inline_kb,
    RecognitionKeyboardButtons,
    recognition_kb,
)
from bot.infrastructure.db.uow import SQLAlchemyUoW
from bot.infrastructure.db.models import NeuralModel
from bot.states import UploadingPhotoForm
from bot.utils import RoboFlow, text_templates

logger = logging.getLogger(__name__)

recognition_router = Router()


@recognition_router.message(F.text == CommonKeyBoardButtons.recognize)
async def upload_image_command(message: Message, state: FSMContext):
    """Process reply keyboard for uploading new photo."""
    await state.set_state(UploadingPhotoForm.waiting_upload)
    await message.answer(
        text=text_templates.new_upload_photo_text(),
        reply_markup=ReplyKeyboardRemove(),
    )


@recognition_router.callback_query(Text(RecognitionKeyboardButtons.no_button))
async def upload_image_state(callback: CallbackQuery, state: FSMContext):
    """Upload another photo using inline kb response."""
    await state.set_state(UploadingPhotoForm.waiting_upload)
    await callback.message.answer(
        text=text_templates.new_upload_photo_text(),
    )
    await callback.answer()


@recognition_router.message(
    UploadingPhotoForm.waiting_upload,
    F.photo,
)
async def process_image(message: Message, state: FSMContext):
    """Catch message with uploaded photo and draw inline kb as reply to message."""
    file_id = message.photo[-1].file_id
    file_unique_id = message.photo[-1].file_unique_id
    chat_id = message.chat.id

    await message.reply(
        text=text_templates.uploaded_photo_text(recognition_kb),
        reply_markup=uploaded_photo_inline_kb(recognition_kb),
    )

    await state.update_data(
        file_id=file_id,
        chat_id=chat_id,
        file_unique_id=file_unique_id,
    )
    await state.set_state(UploadingPhotoForm.answer)


@recognition_router.message(UploadingPhotoForm.waiting_upload)
async def process_document_image(message: Message):
    """Response to user when wrong file was downloaded."""
    await message.answer(text="You need to upload compressed image")


@recognition_router.callback_query(
    UploadingPhotoForm.answer,
    Text(RecognitionKeyboardButtons.yes_button),
)
async def generate_response(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    model: NeuralModel,
    roboflow_api: RoboFlow,
    uow: SQLAlchemyUoW,
):
    """Check for a previous response otherwise save new response from roboflow to db."""
    user_data = await state.get_data()
    file_id = user_data["file_id"]
    file_unique_id = user_data["file_unique_id"]
    chat_id = user_data["chat_id"]
    await bot.send_chat_action(chat_id, action="typing")
    # Save current uploaded image to images
    uploaded_image_id: UUID = await uow.uploaded_images.save_image(
        file_id, file_unique_id, chat_id
    )

    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)  # Save image to bytes

    loop = asyncio.get_event_loop()
    roboflow_response: tuple[
        dict[str, int], bytes
    ] | None = await loop.run_in_executor(  # roboflow package is sync
        None,
        roboflow_api.recognize,
        file_bytes,
        file_path,
    )

    if roboflow_response is not None:
        labels, image_bytes = roboflow_response
        img = BufferedInputFile(image_bytes, f"{file_id}.jpg")

        recognized_image = await callback.message.answer_photo(
            photo=img,
            caption=text_templates.roboflow_success_response(labels),
            reply_markup=make_main_keyboard(),
        )
        recognized_image_id = recognized_image.photo[0].file_id  # type: ignore
        await uow.responses.save_response(
            uploaded_image_id=uploaded_image_id,
            model=model,
            objects=labels,
            recognized_image_id=recognized_image_id,
        )

    else:
        await callback.message.answer(text=text_templates.roboflow_empty_response())
        await uow.responses.save_response(
            uploaded_image_id=uploaded_image_id, model=model
        )

    await uow.commit()
    await callback.answer(text="Redirecting to main menu", show_alert=True)


@recognition_router.callback_query(
    UploadingPhotoForm.answer,
    Text(RecognitionKeyboardButtons.yes_button),
    CheckImageFilter(),
)
async def check_previous_response(
    callback: CallbackQuery,
    model: NeuralModel,
    uow: SQLAlchemyUoW,
    checked_image_id: UUID,
):
    """Response for previously made response."""
    previous_response = await uow.responses.get_response_by_uploaded_image_id(
        uploaded_image_id=checked_image_id, model=model
    )
    if previous_response.recognized_image_id:
        response_text = text_templates.roboflow_success_response(
            previous_response.get_labels()
        )
    else:
        response_text = text_templates.roboflow_empty_response()
    await callback.message.answer_photo(
        photo=previous_response.recognized_image_id,
        caption=response_text,
        reply_markup=make_main_keyboard(),
    )
    await callback.answer(text="Redirecting to main menu", show_alert=True)
