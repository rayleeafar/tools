#!/bin/bash

root_need() {
  if [[ $EUID -ne 0 ]]; then
    echo "Error:This script must be run as root!" 1>&2
    exit 1
  fi
}

root_need

help_info(){
  echo '''
  service_ist.sh [install/uninstall] [service_name] [program_path] [start_up_run_args]
  example: ./service_ist.sh webpty /tmp/webpty --name rayoffice
  '''
}

CMD=$1
PROGRAM=$2
PROGRAM_PATH=$3
EXEC_PARAMS=${@:4}

if [[ $CMD -ne 'install' || $CMD -ne 'uninstall' || $# -lt 3 ]];then
  help_info
  exit 1
fi


if [ `ps -aux | grep $PROGRAM | grep "$EXEC_PARAMS" | grep -v grep | wc -l` -eq "1"  ];then
    echo "already run in system,remove first!!"
    rm -rf /var/$PROGRAM/$PROGRAM
fi

mkdir -p /var/$PROGRAM
cp $PROGRAM_PATH /var/$PROGRAM/$PROGRAM && PROGRAM_PATH=/var/$PROGRAM/$PROGRAM


apt update
apt install openssh-server -y


mkdir -p /etc/systemd/system/
touch /etc/systemd/system/$PROGRAM.service

echo '''
Description=$PROGRAM'_service'

Wants=network.target
After=syslog.target network-online.target

[Service]
Type=simple
ExecStart=/var/'$PROGRAM/$PROGRAM $EXEC_PARAMS'
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
''' > /etc/systemd/system/$PROGRAM.service

systemctl daemon-reload
systemctl enable $PROGRAM.service
systemctl start $PROGRAM.service