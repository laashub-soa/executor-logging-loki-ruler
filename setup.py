import logging

from __init__ import init
from service import loki_ruler

init()
logger = logging.getLogger('setup')
logger.setLevel(logging.DEBUG)
if __name__ == '__main__':
    loki_ruler.loki_ruler()
