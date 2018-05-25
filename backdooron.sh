#!/bin/bash

#sudo apt-get install openssh-server
#ssh-keygen -t rsa
#scp id_rsa.pub ray@app.raylee.com:~/.ssh/authorized_keys
#ssh-copy-id $SERVER_IP

#set app.arylee.com server's ssh config 
#vim /etc/ssh/sshd_config 
#add this line `GatewayPorts yes`
#sudo service ssh restart
#if the scrip is run in office localNET,
#you can connet it on server by `ssh -l <localPC_username> -p <PORT> localhost`
#or on any other network use `ssh <localPC_username>@<SERVER_IP> -p <PORT>`

SERVER_IP=$1
PORT=$2
until ssh -N -R $PORT:localhost:22 $SERVER_IP; do
    echo "reconnect to server $SERVER_IP" >&2
    sleep 3
done
 
