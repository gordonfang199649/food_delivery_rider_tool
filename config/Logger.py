import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="'%(asctime)s : %(filename)s  : %(funcName)s : %(levelname)s : %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
