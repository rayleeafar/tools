#!/bin/bash
#
# use script start screen session,and run command
#

cd /home/lan/fjord
# pipenv shell

# $1 worker dir ; $2 screen session name ; $3 cmd to excute
startScreen(){
    if screen -ls | grep $2 > /dev/null 2>&1; then  
        echo $2,' is already created!'
        echo 'do nothing,return'
        return  
    fi  
    cd $1
    screen -dmS $2
    screen -X -S $2 -p 0 -X stuff $"$3" 
}

startScreen '~' 'user-service' 'python user.py\n'


exit
