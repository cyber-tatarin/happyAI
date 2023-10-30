import asyncio
import uuid
from datetime import datetime
import os
import re

from aiogram.fsm.storage.base import StorageKey
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramNotFound
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram import F

import utils
import g

# конфигурация
# -------------------------------------------------------------------------------------------------

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TG_API'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
admin_ids = {459471362, 983672566, 617595364, 645900005}
# ADMIN_ID = 645900005
ADMIN_ID = 459471362


# -------------------------------------------------------------------------------------------------


class UserStates(StatesGroup):
    i2t_state = State()


@dp.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Добро пожаловать, хозяин..\n\n'
                         'Чтобы попробовать функцию чтения документа, нажмите \n  /upload_doc')


@dp.message(Command('upload_doc'))
async def store_file_ids(message: types.Message, state: FSMContext):
    await message.delete()
    await state.set_state(UserStates.i2t_state)
    await message.answer('Отправьте, пожалуйста, фото паспорта, данные с которого я должен считать')


@dp.message(UserStates.i2t_state, F.content_type.in_({types.ContentType.PHOTO}))
async def set_have_eaten_without_plates(message: types.Message, state: FSMContext):
    message_to_delete = await message.answer('Подождите, пожалуйста, я тружусь...')
    filename = f'{uuid.uuid4().int}.jpg'
    file_path = os.path.join('media', filename)
    await bot.download(message.photo[-1], file_path)
    print('after download')
    try:
        extracted_text = g.google_ocr(file_path)
        print(extracted_text)
        if extracted_text is not None:
            validated_text = utils.gpt_validate(extracted_text)
            print(validated_text)
        else:
            raise Exception

        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as x:
        validated_text = 'Компьютерное видение не смогло распознать текст. Попробуйте загрузить более качественное фото'
        print(x)
    
    await bot.delete_message(message.from_user.id, message_to_delete.message_id)
    await message.answer(f'Вот данные паспорта, фото которого Вы прислали выше, на 2 языках:\n\n{validated_text}\n\n'
                         f'Если Вы хотите загрузить еще фото, нажмите \n/upload_doc')
    await state.clear()


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
    