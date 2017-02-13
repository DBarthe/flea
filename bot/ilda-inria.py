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


INTERVAL_PROPAGATE = 30
INTERVAL_REPORT = 20
INTERVAL_CHECKQUIT = 10


#hostTableSpec = [(10,1,27),(15,1,24),(13,1,24),(12,1,24)]
#hostTableSpec = [(11,23,24)]

STATIC_HOST_TABLE = [
    "a10p1","a10p10","a10p11","a10p12",
    "a10p13","a10p14","a10p15","a10p16",
    "a10p17","a10p18","a10p19","a10p2",
    "a10p20","a10p21","a10p22","a10p23",
    "a10p24","a10p25","a10p26","a10p27",
    "a10p3","a10p4","a10p5","a10p6",
    "a10p7","a10p8","a10p9","a11p1",
    "a11p10","a11p11","a11p12","a11p13",
    "a11p14","a11p15","a11p16","a11p17",
    "a11p18","a11p19","a11p2","a11p20",
    "a11p21","a11p22","a11p23","a11p24",
    "a11p26","a11p3","a11p4","a11p5",
    "a11p6","a11p7","a11p8","a11p9",
    "a12p1","a12p10","a12p11","a12p12",
    "a12p13","a12p14","a12p15","a12p16",
    "a12p17","a12p18","a12p19","a12p2",
    "a12p20","a12p21","a12p22","a12p23",
    "a12p24","a12p26","a12p3","a12p4",
    "a12p5","a12p51","a12p6","a12p7",
    "a12p8","a12p9","a13p1","a13p10",
    "a13p11","a13p12","a13p13","a13p14",
    "a13p15","a13p16","a13p17","a13p18",
    "a13p19","a13p2","a13p20","a13p21",
    "a13p22","a13p23","a13p24","a13p26",
    "a13p3","a13p4","a13p5","a13p50",
    "a13p6","a13p7","a13p8","a13p9",
    "a14p1","a14p10","a14p11","a14p12",
    "a14p13","a14p14","a14p15","a14p16",
    "a14p17","a14p18","a14p19","a14p2",
    "a14p20","a14p21","a14p22","a14p23",
    "a14p24","a14p26","a14p3","a14p4",
    "a14p5","a14p6","a14p7","a14p8",
    "a14p9","a15p1","a15p10","a15p11",
    "a15p12","a15p13","a15p14","a15p15",
    "a15p16","a15p17","a15p18","a15p19",
    "a15p2","a15p20","a15p21","a15p22",
    "a15p23","a15p24","a15p26","a15p3",
    "a15p4","a15p5","a15p6","a15p7",
    "a15p8","a15p9","a16p1","a16p10",
    "a16p11","a16p12","a16p13","a16p14",
    "a16p15","a16p16","a16p17","a16p18",
    "a16p19","a16p2","a16p20","a16p21",
    "a16p22","a16p23","a16p24","a16p26",
    "a16p3","a16p4","a16p5","a16p6",
    "a16p7","a16p8","a16p9",
]


startBotCommand="cd ~/flea/bot && ./start-ilda.sh"

selfHost = socket.gethostname()
logFile = './log/%s.log' % selfHost

logging.basicConfig(filename=logFile,level=logging.DEBUG,
                    format='[%(asctime)s][' + selfHost +'] %(levelname)s: %(message)s')

def datetimeStr():
    return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")

def log(msg):
    print ("[%s]" % datetimeStr(), "%s: " % selfHost, msg.strip())
    sys.stdout.flush()

def makeHostTable():
    table = STATIC_HOST_TABLE
    #for (room,start,end) in hostTableSpec:
    #    table += ["a" + str(room) + "p" + str(machine)
    #             for machine in range(start, end + 1)]
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
    ssh = subprocess.Popen([
        "ssh", "-oStrictHostKeyChecking=no", '-oBatchMode=yes', '-oConnectTimeout=3',
        host, cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    response = res.stdout.decode("utf-8").strip()
    print ("resonse = ", response)
    if response.startswith("HTTP"):
        try:
            body = response.split("\n")[-1]
            logging.info("report sent : [%d] %s", res.returncode, body)
        except:
            loggin.error("strange reponse body: [%d] %s", res.returncode, response)
    else:
        logging.info("report not sent : [%d] %s", res.returncode, response)



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
