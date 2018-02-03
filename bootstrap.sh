#!/bin/bash

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
sudo -H pip3 install virtualenv
cd /vagrant
source flask_env/bin/activate/
pip install -r requirements.txt