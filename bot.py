#!/usr/bin/env python3

import sys
import subprocess
import random
import time
import datetime

hostTableSpec = [(1, 1, 25),
                 (2, 1, 15),
                 (3, 1, 34)]

startBotCommand="cd ~/git/flea && ./start-bot.sh"

def makeHostTable():
    table = []
    for (room,start,end) in hostTableSpec:
        table += ["a" + str(room) + "p" + str(machine)
                 for machine in range(start, end + 1)]
    return table    

hostTable = makeHostTable()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def executeOverSSH(host, cmd):
    ssh = subprocess.Popen(["ssh", host, cmd],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
    for line in ssh.stdout.readlines():
        print (line.decode("utf-8"))
    for line in ssh.stderr.readlines():
        print ("error:", line.decode("utf-8"))
    
def propagateRandomly():
    executeOverSSH(random.choice(hostTable), startBotCommand)

def main():
    while True:
        print("[%s]" % str(datetime.datetime.now()), "I'm here")
        propagateRandomly()
        time.sleep(1)

    
if __name__ == "__main__":
    main()
