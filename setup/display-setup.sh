#! /usr/bin/env bash
set -euo pipefail

# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
# --- CIRCUITPYTHON PREP ---
# environment setup
sudo apt-get install -y python3-pip python3-setuptools python3-venv

cd ~
python3 -m venv env --system-site-packages
source ~/env/bin/activate

# --- ADAFRUIT BLINKA SETUP ---
# adapted from manual process
# pi config
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial_hw 0
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint disable_raspi_config_at_boot 0

# install dependencies
sudo apt-get install -y i2c-tools libgpiod-dev python3-libgpiod
pip3 install --upgrade adafruit-blinka adafruit-python-shell click 

# fix pi cs pins
# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices#reassigning-or-disabling-the-spi-chip-enable-lines-3097985
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/raspi-spi-reassign.py
sudo -E env PATH=$PATH python3 raspi-spi-reassign.py --ce0=disabled --ce1=disabled
rm raspi-spi-reassign.py

# --- DISPLAY SETUP ---
# https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup
# install display packages
sudo apt-get install -y fonts-dejavu python3-pil python3-numpy
pip3 install adafruit-circuitpython-rgb-display
pip3 uninstall -y RPi.GPIO

# --- ENABLE AUTOMATIC LAUNCH ---
mkdir -p ~/.config/systemd/user/
cp ~/Desktop/robot-software/setup/display-stats.service ~/.config/systemd/user
systemctl --user enable --now display-stats.service