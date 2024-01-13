#!/usr/bin/env bash

echo -n "Generating service file... "
echo "
[Unit]
Description=MASSA Remote Monitoring service
Wants=network.target
After=network.target

[Service]
Type=idle
User=$USER
WorkingDirectory=$HOME/massa_rmon
ExecStart=$HOME/massa_rmon/bin/python3 main.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
" > ./massa_rmon.service

if [[ $? -eq 0 ]]
then
        echo "Done!"
else
        echo "Error!"
        exit 1
fi


echo "Copying service file to /etc/systemd/system/massa_rmon.service... "
sudo cp ./massa_rmon.service /etc/systemd/system/massa_rmon.service

if [[ $? -eq 0 ]]
then
        echo "Done!"
else
        echo "Error!"
        exit 1
fi


echo -n "Reloading systemd daemon configuration... "
sudo systemctl daemon-reload

if [[ $? -eq 0 ]]
then
        echo "Done!"
else
        echo "Error!"
        exit 1
fi


echo
echo "Success!"
