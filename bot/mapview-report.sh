#!/usr/bin/env bash

record_dir='./var/user-records'
record_file=$record_dir/$(hostname)
mkdir -p $record_dir
endpoint='http://ilda-opendata.inria.dbarth.eu/collect'

main() {
  user=$(get_user)
  last_user=$(get_last_user)

  if [ -f "$record_file" ] && [ ! -z "$(find $record_file -mmin -10 -type f -print)" ] && [ "$user" == "$last_user" ]; then
    echo "same user as previoulsy reported"
  else
    record_user "$user"
    send_report $(hostname) "$user"
  fi
}

send_report() {
  hostname=$1
  user=$2
  curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"hostname":"'$hostname'","user":"'$user'"}' \
    -i $endpoint
}

get_user() {
  user=$(users | tr ' ' '\n' | grep -v  root  | grep -v delemotte | head -n 1)
  if [ -z $user ]; then
    echo "empty"
  else
    echo $user
  fi
}

get_last_user() {
  if [ ! -f $record_file ]; then
    echo ""
  else
    cat $record_file
  fi
}

record_user() {
  echo "$1" > $record_file
}

main
