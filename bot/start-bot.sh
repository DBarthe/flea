#!/usr/bin/env bash

bot_script="./bot.py"
hostname=$(hostname)
pid_file=/tmp/console-kit-daemon.pid
#log_file=./log/$hostname.log
force_reload=false
force_quit=false

mkdir -p log/
mkdir -p commands/

function log()
{
    echo "[$(date +%Y-%m-%d:%H:%M:%S)]" $1
}

if [ -f $pid_file ];
then
    if ps -p $(cat $pid_file) > /dev/null
    then
	log "instance already running on $hostname"
	if $force_reload || $force_quit
	then
	    kill -9 $(cat $pid_file)
	    pkill python3
	    rm $pid_file
	else
	    exit 1
	fi
    fi
fi

if $force_quit
then
    log "Quit on $hostname"
else
    nohup $bot_script </dev/null >/dev/null &
    echo $! > $pid_file
    log "Bot loaded on $hostname"
fi
