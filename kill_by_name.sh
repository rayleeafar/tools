#!/bin/bash

#if [ $# -eq 0 ]
if [ -z "$1" ]
  then
    echo "No process name supplied"
    exit 1
fi
NAME=$1
ps -aux | grep -v grep | grep -v $0 | grep $NAME
echo "#####-------------------------------------------------------------------------------#####"
read -p 'Are you sure to kill above process? ctrl+c abort else hit anykey to continue' careless

kill -9 $(ps -aux | grep -v grep | grep -v $0 | grep $NAME | gawk '{print $2}')
