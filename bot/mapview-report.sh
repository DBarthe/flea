#!/usr/bin/env bash

sendReport() {
  hostname=$1
  user=$2
  curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"hostname":"'$hostname'","user":"'$user'"}' \
    -i http://dbarth.eu:3000/collect
}

getUser() {
  users | cut -f 1 -d " "
}

sendReport $(hostname) $(getUser)
