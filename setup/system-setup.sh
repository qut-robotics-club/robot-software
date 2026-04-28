#!/usr/bin/env bash
set -euo pipefail

# update the system
sudo apt-get update
sudo apt-get upgrade -y

# enable and install VNC
sudo apt-get install realvnc-vnc-server -y
sudo raspi-config nonint do_vnc 0

# install needed packages
sudo apt-get install python3-opencv -y
# flask?