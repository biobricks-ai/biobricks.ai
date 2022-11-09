#!/bin/bash

export $(echo $(cat env_test.env | sed 's/#.*//g'| xargs) | envsubst)

python3 src/main.py bbportal &
pid=$!

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# SELECTED_WID=$(($(xwininfo | grep "Window id" | cut -d " " -f 4)))

inotifywait -q -m -e close_write ./src/bbportal/templates |
while read -r filename event; do
  
  echo killing $pid
  kill $pid
  python3 src/main.py bbportal &
  pid=$!
  echo $pid

#   sleep 0.5
#   echo "File changed... Sending F5 to window id=$SELECTED_WID"
#   CURRENT_WID=$(xdotool getwindowfocus)
#   xdotool windowactivate $SELECTED_WID
#   xdotool key F5
#   xdotool windowactivate $CURRENT_WID
  
done