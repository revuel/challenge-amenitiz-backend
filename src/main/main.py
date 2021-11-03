""" Main module """
import asyncio
import uvicorn

from src.main.application.prefill_service import Prefill
from src.main.infrastructure.database.setup import init_db
from src.main.infrastructure.logging.logger import LOGGER


def main():
    """ Application entry point """
    LOGGER.info('Starting application...')
    init_db()
    asyncio.run(Prefill.all())
    uvicorn.run(
        'src.main.presentation.rest.setup:app',
        host='0.0.0.0',
        port=8000,
        log_level='debug',
    )

