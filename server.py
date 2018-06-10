import conf
import subprocess
import socket
import threading
import time
from plot import update_plot
from logger import logger

exit = False


def socket_handler(id, ip):
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
    while not exit:
        client_data = conn.recv(1024).decode()
        try:
            update_plot(client_data)
        except Exception as e:
            logger.error(str(e) + ': ' + client_data)

        # conn.sendall('sever have received your message'.encode())  # send feedback to client
    conn.close()
    logger.info(socket_logger_head + "antenna socket is closed")


ports = {}  # key: ip, value: port
logger.info("start to set each antenna...")
for id, prop in conf.ANTENNAS.items():

    threading.Thread(target=socket_handler, args=(id, prop['IP'])).start()
    while prop['IP'] not in ports:
        time.sleep(0.1)
    logger_head = "[antenna " + prop['IP'] + ":" + str(ports[prop['IP']]) + "] "
    if conf.RUN_ANTENNAS:
        #  args:  $1: antenna ip, $2: server ip,  $3: port, $4: run_antennas
        subprocess.Popen(["sh", "antenna.sh", prop["IP"], conf.SERVER, str(ports[prop["IP"]]), "1"])
        logger.info(logger_head + "file transfer completed")
        logger.info(logger_head + "antenna socket is started")
    else:
        subprocess.Popen(["sh", "antenna.sh", prop['IP'], conf.SERVER, str(ports[id]), "0"])
        logger.info(logger_head + "antenna socket isn't started")

logger.info("antennas setting are finished")

