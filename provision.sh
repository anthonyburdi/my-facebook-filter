#!/usr/bin/env bash

## Update and Install Dependencies
echo updating...
apt-get update > /dev/null
echo done

echo upgrading...
apt-get upgrade -y >/dev/null
echo done
apt-get install -y git
apt-get -y install python-pip
pip install virtualenv

## Set Up Virtual Environment, Install Dependencies
cd /vagrant
virtualenv venv
source venv/bin/activate
pip install -r /vagrant/requirements.txt

## Start Flask App
python mytoday.py