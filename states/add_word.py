"""
FSM состояния для добавления слова.
"""

from aiogram.fsm.state import State, StatesGroup


class AddWordState(StatesGroup):
    """Состояния при добавлении нового слова."""
    waiting_for_word = State()  # Ожидание ввода английского слова


class TrainingState(StatesGroup):
    """Состояния во время тренировки."""
    in_training = State()  # Пользователь проходит тренировку
