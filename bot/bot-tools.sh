#!/usr/bin/env bash

command_dir='./commands'
command_quit_file=$command_dir/quit
log_dir='./log'

mkdir -p log/
mkdir -p commands/

start() {
  echo "0" > $command_quit_file
  ./start-bot.sh
}

stop() {
  echo "1" > $command_quit_file
}

log() {
  tail -f $log_dir/*
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
    *)
        echo $"Usage: $0 {start|stop|log}"
        exit 1
esac
