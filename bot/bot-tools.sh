#!/usr/bin/env bash

command_dir='./commands'
command_quit_file=$command_dir/quit
command_start='./start-bot.sh'
log_dir='./log'

mkdir -p log/
mkdir -p commands/

start() {
  echo "0" > $command_quit_file
  $command_start
}

stop() {
  echo "1" > $command_quit_file
}

log() {
  tail -f $log_dir/*
}

log_clear() {
  truncate --size 0 $log_dir/*
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    log)
        log
        ;;
    log-clear)
	log_clear
	;;
    *)
        echo $"Usage: $0 {start|stop|log}"
        exit 1
esac
