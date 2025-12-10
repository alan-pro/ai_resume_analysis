import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_path: str = "logs/app.log"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))

    # File rotating
    fh = RotatingFileHandler(log_path, maxBytes=2*1024*1024, backupCount=5, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))

    logger.addHandler(ch)
    logger.addHandler(fh)
