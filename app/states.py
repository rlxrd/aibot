from aiogram.fsm.state import State, StatesGroup


class Chatting(StatesGroup):
    question = State()
    answer = State()
