import logging
import os

LOG_DIR = './logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# file handler
fh = logging.FileHandler(os.path.join(LOG_DIR, 'app.log'))
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

logger.addHandler(fh)