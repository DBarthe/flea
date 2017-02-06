#!/usr/bin/env python3

import sys
import subprocess
import random
import time
import datetime
import socket
import atexit
from threading import Thread

hostTableSpec = [(10, 1, 2)]

startBotCommand="cd ~/flea/bot && ./start-bot.sh"

selfHost = socket.gethostname()

def datetimeStr():
    return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")

def log(msg):
    print ("[%s]" % datetimeStr(), "%s: " % selfHost, msg)
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
    log ("killing processes...")
    for p in subProcessList:
        p.kill()

def executeOverSSH(host, cmd):
    log("ssh %s %s" % (host, cmd))
    ssh = subprocess.Popen(["ssh", "-oStrictHostKeyChecking=no", host, cmd],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    subProcessList.append(ssh)
    for line in ssh.stdout.readlines():
        print (line.decode("utf-8"))
    for line in ssh.stderr.readlines():
        print ("error:", line.decode("utf-8"))

def propagateRandomly():
    executeOverSSH(random.choice(hostTable), startBotCommand)


def propagateAllOnce():
    for host in hostTable:
        executeOverSSH(host, startBotCommand)

quitCommandFile = './commands/quit'
def hasToQuit():
    log("check command file")
    try:
        f = open(quitCommandFile, 'r')
        content = f.read()
        f.close()
        return int(content)
    except:
        return False

def main():
    atexit.register(killSubProcesses)
    i = 0
    while True:
        if i % 1 == 0:
            if hasToQuit():
                log("command quit accepted")
                exit(0)
        log("I'm here (%d)" % i)
        propagateRandomly()
        time.sleep(1)
        i += 1

if __name__ == "__main__":
    main()