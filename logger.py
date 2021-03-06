import logging
import conf
import datetime

# main logger
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
# add file handler
fh = logging.FileHandler('main.log', mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s - %(asctime)s] %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# set file name


# # add file handler rawData_logger
# rawData_logger = logging.getLogger("rawData")
# rawData_logger.propagate = conf.SHOW_MSG
# rawData_logger.setLevel(logging.DEBUG)
#
# rawData_fh = logging.FileHandler(conf.FILE_PATH + "rawData" + filename, mode='w')
# rawData_fh.setLevel(logging.DEBUG)
# rawData_fh.setFormatter(logging.Formatter('%(message)s'))
# rawData_logger.addHandler(rawData_fh)
#
# # add file handler data_logger
# data_logger = logging.getLogger("data")
# data_logger.propagate = conf.SHOW_MSG
# data_logger.setLevel(logging.DEBUG)
#
# data_fh = logging.FileHandler(conf.FILE_PATH + "data" + filename, mode='w')
# data_fh.setLevel(logging.DEBUG)
# data_fh.setFormatter(logging.Formatter('%(message)s'))
# data_logger.addHandler(data_fh)
