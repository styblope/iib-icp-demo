#~/bin/bash

while true
do
    ./wrk -c 100 -t 20 -d 1 $1 | grep Requests
done
