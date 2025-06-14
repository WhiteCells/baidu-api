import os
import logging
import json
from app.utils.config import Config


def get_logger(table_name):
    os.makedirs(Config.WORKER_DIR, exist_ok=True)
    logger = logging.getLogger(table_name)
    path = os.path.join(Config.WORKER_DIR, f"{os.getpid()}_{table_name}.log")
    handler = logging.FileHandler(path)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def get_progress(table_name):
    os.makedirs(Config.PROGRESS_DIR, exist_ok=True)
    path = os.path.join(Config.PROGRESS_DIR, f"{table_name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return int(json.load(f).get("last_index", 0))
    return 0


def save_progress(table_name, index):
    path = os.path.join(Config.PROGRESS_DIR, f"{table_name}.json")
    with open(path, "w") as f:
        json.dump({"last_index": index}, f)