from aiogram.fsm.state import StatesGroup, State


class ResponseStates(StatesGroup):
    paginated_response = State()
