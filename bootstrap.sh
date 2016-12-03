#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y apache2

# Repair "==> default: stdin: is not a tty" message
sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile
# Git
echo 'Installing Git...'
#sudo apt-get -y install git
sudo apt-get -y install git > /dev/null 2>&1
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi