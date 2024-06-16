from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='💬 Text'), KeyboardButton(text='🌠 Image')],
    [KeyboardButton(text='🎙 Voice'), KeyboardButton(text='⚙️ Profile')]
], input_field_placeholder='✨ Generate...')


async def back_model_text(tg_id, model):
    pass
