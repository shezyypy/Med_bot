from aiogram.fsm.state import StatesGroup, State


class TemperatureStates(StatesGroup):
    waiting_for_temperature = State()
