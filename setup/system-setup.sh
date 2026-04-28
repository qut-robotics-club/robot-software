#!/usr/bin/env bash
set -euo pipefail

cat ./initramfs | sudo tee /etc/initramfs-tools/initramfs.conf 1&>/dev/null 
# update the system
sudo apt-get update
sudo apt-get upgrade -y

# enable and install VNC
sudo apt-get install realvnc-vnc-server -y
sudo raspi-config nonint do_vnc 0

# install needed packages
sudo apt-get install python3-opencv -y
# flask?