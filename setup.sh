#!/usr/bin/env bash
# fix bad NTP defaults (can't access default NTP pool on QUT networks)
sudo sed -i -e "s/#NTP=/NTP=pool.ntp.org/g" /etc/systemd/timesyncd.conf
sudo timedatectl set-ntp False
sudo timedatectl set-ntp True

# update the system
sudo apt-get update
sudo apt-get full-upgrade -y

# enable and install VNC
sudo apt-get install realvnc-vnc-server -y
sudo raspi-config nonint do_vnc 0

# install needed packages
sudo apt-get python3-opencv -y

cd ~
git clone https://github.com/qut-robotics-club/robot-software
cd robot-software
