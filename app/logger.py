import logging

logger = logging.getLogger('flask_forum')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('flask_forum_dbg.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(level)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)


