#!/usr/bin/env bash
set -euo pipefail

# fix NTP time if it hasn't been already
./fix-time.sh
# update and install needed packages
./system-setup.sh
# setup the display (to show stats)
./display-setup.sh

# add automatic python environment setup to bashrc
ENV_SOURCE="source ~/env/bin/activate"
if grep -fq "$ENV_SOURCE" "~/.bashrc"; then
  echo "Environment source already enabled!"
else
  echo "Adding environment sourcing..."
  echo "$ENV_SOURCE" >> ~/.bashrc
fi
echo "Please run \"source ~/env/bin/activate\" to activate the python environment"
echo "Rebooting in 5 seconds to apply changes... CTRL+C to cancel"
sleep 5
sudo reboot