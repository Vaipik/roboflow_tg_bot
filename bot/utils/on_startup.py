from bot.config import NeuralNetwork
from bot.db.models import NeuralModel
from bot.db.repository import NeuralModelRepository


async def get_model(nn_params: NeuralNetwork, sessionmaker) -> NeuralModel:
    """Check presence of current neural model in db."""
    async with sessionmaker() as session:
        nn_repo = NeuralModelRepository(session)
        model = await nn_repo.check_on_startup(nn_params.name, nn_params.version)
        if model is not None:
            return model
        model = await nn_repo.insert_on_startup(nn_params.name, nn_params.version)
        return model
