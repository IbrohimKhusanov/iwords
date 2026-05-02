"""
FSM states for add word and training.
"""

from aiogram.fsm.state import State, StatesGroup


class AddWordState(StatesGroup):
    waiting_for_word = State()


class TrainingState(StatesGroup):
    picking_mode = State()
    translation_answer = State()
    sentence_answer = State()
