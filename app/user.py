from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.states import Chatting
import app.database.requests as rq
import app.keyboards as kb

import re
import app.text as text


from app.generators import Generate

user = Router()
ai = Generate()


async def remove_markdown(text):
    text = re.sub(r'[_*`]', '', text)
    return text


@user.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(tg_id=message.from_user.id)
    await message.answer(text=text.greetings,
                         reply_markup=kb.main)


@user.message(F.text == '💬 Текст')
async def kb_chatgpt(message: Message, state: FSMContext):
    await state.set_state(Chatting.question)
    await message.answer(f'To start a dialogue, send a text or picture to the chat ⬇️')


@user.message(F.text == '🌠 Генерация картинок')
async def kb_image(message: Message):
    await message.answer('This feature is under development.')


@user.message(F.text == '🎙 Голос')
async def kb_voice(message: Message):
    await message.answer('This feature is under development.')


@user.message(F.text == '⚙️ Мой профиль')
async def kb_profile(message: Message):
    user_info = await rq.get_user(tg_id=message.from_user.id)
    await message.answer(f'ID: {user_info.id}\nBalance: {user_info.balance}$')


@user.message(F.photo)
@user.message(Chatting.question, F.photo)
async def chatgpt_question_photo(message: Message, state: FSMContext):
    await message.answer('This feature is under development.')


@user.message(Chatting.answer)
async def chatgpt_answer(message: Message):
    await message.answer('Please wait, the response is being generated.')


@user.message()
@user.message(Chatting.question)
async def chatgpt_question(message: Message, state: FSMContext):
    await state.set_state(Chatting.answer)
    data = await rq.user_text(message.from_user.id)
    try:
        response = await ai.get_model_text(data['company'].sys_name, data['model_variant'].sys_name, message.text)
    except Exception as e:
        print(e)
        try:
            response = await ai.get_model_text(data['company'].sys_name, data['model_variant'].sys_name, message.text)
        except Exception as e:
            print(e)
            await message.answer('Error', reply_markup=kb.main)
            await state.clear()
            return
    try:
        await message.answer(response, parse_mode='Markdown')
    except Exception as e:
        print(e)
        try:
            await message.answer(await remove_markdown(response))
        except Exception as e:
            print(e)
            try:
                await message.answer(response)
            except Exception as e:
                print(e)
                await message.answer('Error.')
    await state.clear()
