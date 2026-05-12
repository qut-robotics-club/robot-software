#!/usr/bin/env bash
set -euo pipefail

# update the system
if ! sudo apt-get update; then
    echo "Failed to update package lists!"
    echo "If this is a fresh image, YOUR SD CARD IS CORRUPTED!"
    exit 1
fi

if ! sudo apt-get upgrade -y; then
    echo "Failed to upgrade packages!"
    echo "If this is a fresh image, YOUR SD CARD IS CORRUPTED!"
    exit 1
fi

# enable and install VNC
sudo apt-get install realvnc-vnc-server -y
sudo raspi-config nonint do_vnc 0

# fix localisation
sudo sed -i -e "s|timezone: .*|timezone: Australia/Brisbane|g" /boot/firmware/user-data
sudo timedatectl set-timezone Australia/Brisbane
