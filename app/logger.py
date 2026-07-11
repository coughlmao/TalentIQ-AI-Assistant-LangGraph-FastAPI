# app/logger.py

import logging
import os
import sys

# Compute the target logging severity dynamically
log_level = logging.DEBUG if os.getenv("DEBUG") else logging.INFO

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("talentiq-assistant")
