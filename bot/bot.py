#!/usr/bin/env python3

import sys
import subprocess
import random
import time
import datetime
import socket
import atexit
from threading import Thread
import logging


#hostTableSpec = [(10,1,27),(15,1,24),(13,1,24),(12,1,24)]
hostTableSpec = [(11,23,24)]

startBotCommand="cd ~/flea/bot && ./start-bot.sh"

selfHost = socket.gethostname()
logFile = './log/%s.pid' % selfHost

logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='[%(asctime)s][' + selfHost +'] %(levelname)s: %(message)s')

def datetimeStr():
    return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")

def log(msg):
    print ("[%s]" % datetimeStr(), "%s: " % selfHost, msg.strip())
    sys.stdout.flush()

def makeHostTable():
    table = []
    for (room,start,end) in hostTableSpec:
        table += ["a" + str(room) + "p" + str(machine)
                 for machine in range(start, end + 1)]
    table = [ host for host in table if host != selfHost ]
    return table

hostTable = makeHostTable()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

subProcessList = []
def killSubProcesses():
    logging.info("killing processes...")
    for p in subProcessList:
        p.kill()

def executeOverSSH(host, cmd):
    logging.info("ssh %s %s" % (host, cmd))
    ssh = subprocess.Popen(["ssh", "-oStrictHostKeyChecking=no", host, cmd],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    subProcessList.append(ssh)
    for line in ssh.stdout.readlines():
        logging.info(line.decode("utf-8").strip())
    for line in ssh.stderr.readlines():
        logging.error(line.decode("utf-8").strip())

def propagateRandomly():
    if len(hostTable) > 0:
        executeOverSSH(random.choice(hostTable), startBotCommand)

def propagateAllOnce():
    for host in hostTable:
        executeOverSSH(host, startBotCommand)

quitCommandFile = './commands/quit'
def hasToQuit():
    logging.info("check command file")
    try:
        f = open(quitCommandFile, 'r')
        content = f.read()
        f.close()
        return int(content)
    except:
        return False


def sendReport():
    logging.info("sending report...")
    res = subprocess.run(["./mapview-report.sh"], stdout=subprocess.PIPE)
    response = res.stdout.decode("utf-8")
    print ("resonse = ", response)
    if response.startswith("HTTP"):
        try:
            body = response.split("\n")[-1]
            logging.info("report sent : [%d] %s", res.returncode, body)
        except:
            loggin.error("strange reponse body: [%d] %s", res.returncode, response)
    else:
        logging.info("report not sent : [%d] %s", res.returncode, response)


INTERVAL_PROPAGATE = 60
INTERVAL_REPORT = 30
INTERVAL_CHECKQUIT = 10

def main():
    atexit.register(killSubProcesses)
    i = 0
    while True:
        if i % 60 == 0:
            logging.info("I'm here (%d)" % i)

        if (i+1) % INTERVAL_CHECKQUIT == 0:
            if hasToQuit():
                logging.info("command quit accepted")
                exit(0)

        if (i+0) % INTERVAL_PROPAGATE == 0:
            propagateRandomly()

        if (i + 2) % INTERVAL_REPORT == 0:
            sendReport()

        time.sleep(1)
        i += 1

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("unhandled exception: %s", str(e))
        exit(1)
