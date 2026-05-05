#!/usr/bin/env bash
set -euo pipefail

# update the system
if ! sudo apt-get update; then
    # probably invalid merge lists
    sudo rm -vf /var/lib/apt/lists/*
    # try again
    sudo apt-get update
fi

if ! sudo apt-get upgrade -y; then
    # probably initramfs corrupted
    cat ./initramfs | sudo tee /etc/initramfs-tools/update-initramfs.conf 1>/dev/null 
    # aaand try again
    sudo apt-get upgrade -y
fi

# enable and install VNC
sudo apt-get install realvnc-vnc-server -y
sudo raspi-config nonint do_vnc 0

# install needed packages
sudo apt-get install python3-opencv -y