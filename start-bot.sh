#!/usr/bin/env bash

bot_script="./bot.py"
hostname=$(hostname)
pid_file=/tmp/flea.pid
log_file=./log/$hostname.log
force_reload=true

if [ -f $pid_file ]; 
then
    if ps -p $(cat $pid_file) > /dev/null
    then
	if $force_reload
	then
	    kill -9 $(cat $pid_file)
	else
	    exit 1
	fi
    fi
fi

nohup $bot_script </dev/null >> $log_file &
echo $! > $pid_file
echo "Bot loaded on $hostname"
