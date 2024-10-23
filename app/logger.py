import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

logger.info('Logger configured')
