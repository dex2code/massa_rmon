#!/usr/bin/env bash

sudo systemctl stop massa_rmon.service
sudo systemctl disable massa_rmon.service

rm -rf ~/massa_rmon

sudo rm /etc/systemd/system/massa_rmon.service
sudo systemctl daemon-reload

echo
echo "Service uninstalled!"
echo
