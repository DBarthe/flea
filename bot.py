#!/usr/bin/env python3

import sys
import subprocess
import random
import time
import datetime
import socket


hostTableSpec = [(10, 1, 25)]

startBotCommand="cd ~/flea && ./start-bot.sh"

selfHost = socket.gethostname()

def log(msg):
    print ("[%s]" % str(datetime.datetime.now()), "%s: " % selfHost, msg)

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

def executeOverSSH(host, cmd):
    log("ssh %s %s" % (host, cmd)) 
    ssh = subprocess.Popen(["ssh", "-oStrictHostKeyChecking=no", host, cmd],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
    for line in ssh.stdout.readlines():
        print (line.decode("utf-8"))
    for line in ssh.stderr.readlines():
        print ("error:", line.decode("utf-8"))
    
def propagateRandomly():
    executeOverSSH(random.choice(hostTable), startBotCommand)


def propagateAllOnce():
    for host in hostTable:
        executeOverSSH(host, startBotCommand)

def main():
    propagateAllOnce()
    exit(0)
    
    while True:
        log("I'm here")
        propagateRandomly()
        time.sleep(1)

if __name__ == "__main__":
    main()
