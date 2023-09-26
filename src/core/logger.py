import os
import logging.config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def configure_logger() -> None:
    logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.conf'), disable_existing_loggers=False)
