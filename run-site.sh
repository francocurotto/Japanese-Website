#!/bin/sh
ip=`hostname -I | sed 's/ //g'`
echo Your IP address is $ip. Running the website...
hugo server -D --bind $ip &
xdg-open http://$ip:1313
