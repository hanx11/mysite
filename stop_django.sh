#!/bin/bash

#killall -s INT uwsgi
file=django.pid
if [ -f $file ]; then
    kill -9 `cat $file`
    rm $file
    echo "Stop $file"
fi
