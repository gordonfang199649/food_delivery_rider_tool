import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="'%(asctime)s : %(filename)s  : %(funcName)s : %(levelname)s : %(message)s",
    handlers=[
        logging.FileHandler("log_file.log", 'w', 'utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
