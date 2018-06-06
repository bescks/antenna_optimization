import logging
import time

logging.basicConfig(format=('[%(name)s - %(levelname)s - %(asctime)s] %(message)s'))

# main logger
logger = logging.getLogger("Main")
logger.setLevel(logging.DEBUG)
# add file handler
fh = logging.FileHandler('main.log', mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s - %(asctime)s] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# data_logger
data_logger = logging.getLogger("Data")
data_logger.setLevel(logging.DEBUG)
# add file handler
data_fh = logging.FileHandler('data.csv', mode='w')
data_fh.setLevel(logging.DEBUG)
data_formatter = logging.Formatter('%(message)s')
data_fh.setFormatter(data_formatter)
data_logger.addHandler(data_fh)

# i = 0
# while True:
#     time.sleep(1)
#     logger.info(i)
#     data_logger.info("2 " + str(i))
#     i += 1
