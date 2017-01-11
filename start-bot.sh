#!/usr/bin/env bash

bot_script="./bot.py"
hostname=$(hostname)
pid_file=/tmp/flea-$hostame.pid
log_file=./log/$hostname.log

if [ -f $pid_file ]; 
then
    if ps -p $(cat $pid_file) > /dev/null
    then
	echo "error: already existing instance running"
	exit 1
    fi
fi

nohup $bot_script > $log_file &
echo $! > $pid_file
