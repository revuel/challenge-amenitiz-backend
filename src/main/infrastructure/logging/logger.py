""" Logging module """
import logging

logging.basicConfig(level='DEBUG', format='%(asctime)-15s %(funcName)-20s > %(message)s')
logging.getLogger('sqlalchemy').propagate = False

LOGGER = logging.getLogger()
