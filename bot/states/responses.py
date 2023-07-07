from aiogram.fsm.state import StatesGroup, State


class ResponseStates(StatesGroup):
    """State for responses handler."""

    paginated_response = State()
