
import logging
import os
from datetime import datetime

# logging.basicConfig(level=logging.INFO, filename="/home/pi/Artemis-Alpha/Code/log/log_" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ".log", 
# filemode="w", format="%(asctime)s - %(levelname)s - %(filename)s/%(funcName)s  - %(message)s")
# logging.info("main.py started")

logging_dir = os.path.join(os.path.dirname(__file__), "log")
if not os.path.exists(logging_dir):
    os.makedirs(logging_dir)
logging_file = os.path.join(logging_dir, "log_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log")

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(logging_file),
        logging.StreamHandler()
    ]
)

logging.info("logging started")

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

logger = logging.getLogger("")

def log(level, msg, *args, **kwargs):
    logger.log(level, msg, *args, **kwargs)    