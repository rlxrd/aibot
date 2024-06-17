from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

from app.states import Chatting
import app.database.requests as rq

import os
import re
import time
import random
import PIL.Image
import app.text as text
from config import GEMINI

import google.generativeai as genai


user = Router()
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel('gemini-1.5-flash')


async def remove_markdown(text):
    text = re.sub(r'[_*`]', '', text)
    return text


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await rq.set_user(tg_id=message.from_user.id)
    await message.answer(text=text.greetings, reply_markup=ReplyKeyboardRemove())
    await state.clear()


@user.message(F.photo)
@user.message(Chatting.question, F.photo)
async def chatgpt_question_photo(message: Message, state: FSMContext):
    await state.set_state(Chatting.answer)
    rrand = random.randint(1, 9999)
    ddate = time.time()
    await message.bot.download(file=message.photo[-1].file_id, destination=f'ph{rrand}{ddate}.jpg')
    img = PIL.Image.open(f'ph{rrand}{ddate}.jpg')
    response = model.generate_content(img)
    os.remove(f'ph{rrand}{ddate}.jpg')
    try:
        await message.answer(response.text, parse_mode='Markdown')
    except:
        try:
            await message.answer(await remove_markdown(response.text))
        except:
            try:
                await message.answer(response.text)
            except Exception as e:
                print(e)
                await message.answer('Error №2. Please contact support: @mesudoteach')
    await state.clear()


@user.message()
@user.message(Chatting.question)
async def chatgpt_question(message: Message, state: FSMContext):
    await state.set_state(Chatting.answer)
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action=ChatAction.TYPING)

    try:
        chat = (await state.get_data())['context']
        if len(chat.history) > 10:
            chat = model.start_chat(history=[])
        response = chat.send_message(message.text)
        await state.update_data(context=chat)
    except:
        chat = model.start_chat(history=[])
        response = chat.send_message(message.text)
        await state.update_data(context=chat)

    try:
        await message.answer(response.text, parse_mode='Markdown')
    except:
        try:
            await message.answer(await remove_markdown(response.text))
        except:
            try:
                await message.answer(response.text)
            except Exception as e:
                print(e)
                await message.answer('Error №1. Please contact support: @mesudoteach')
    await state.set_state(Chatting.question)


@user.message(Chatting.answer)
async def chatgpt_answer(message: Message):
    await message.answer('Please wait, the response is being generated.')
