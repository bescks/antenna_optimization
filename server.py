import conf
import subprocess
import socket
import threading
import time
from logger import logger, data_logger

conn_flag = True


def socket_handler(ip):
    """
    this function is only invoked by thread and responsible for managing communication  between server and antenna
    :param ip: antenna's ip
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP socket
    sk.bind(('', 0))
    global ports
    ports[ip] = sk.getsockname()[1]
    socket_logger_head = "[" + ip + ":" + str(ports[ip]) + "] "
    sk.listen(5)
    logger.info(socket_logger_head + "server socket has been created")
    conn, address = sk.accept()
    while conn_flag:
        client_data = conn.recv(1024).decode()
        data_logger.info(client_data)
        # conn.sendall('sever have received your message'.encode())  # send feedback to client
    conn.close()
    logger.info(socket_logger_head + "antenna socket is closed")


ports = {}
logger.info("start to set each antenna...")
for ip, prop in conf.ANTENNAS.items():
    threading.Thread(target=socket_handler, args=(ip,)).start()
    while ip not in ports:
        time.sleep(0.1)
    logger_head = "[antenna " + ip + ":" + str(ports[ip]) + "] "
    if conf.RUN_ANTENNAS:
        #  args:  $1: antenna ip, $2: server ip,  $3: port, $4: run_antennas
        subprocess.Popen(["sh", "antenna.sh", ip, conf.SERVER, str(ports[ip]), "1"])
        logger.info(logger_head + "file transfer completed")
        logger.info(logger_head + "antenna socket is started")
    else:
        subprocess.Popen(["sh", "antenna.sh", ip, conf.SERVER, str(ports[ip]), "0"])
        logger.info(logger_head + "antenna socket isn't started")

logger.info("antennas setting are finished")
