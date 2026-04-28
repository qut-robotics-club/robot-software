#!/usr/bin/env bash
set -euo pipefail
# fix bad NTP defaults (can't access default NTP pool on QUT networks)
sudo sed -i -e "s/#NTP=/NTP=pool.ntp.org/g" /etc/systemd/timesyncd.conf
sudo timedatectl set-ntp False
sudo timedatectl set-ntp True