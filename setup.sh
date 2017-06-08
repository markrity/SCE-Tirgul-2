#!/bin/bash

#update system
sudo yum -y update && upgrade

#install git python and devtools
sudo yum -y install git-all centos-relese-SCL python-setuptools python-setuptools-devel python-devel yum-utils
sudo yum -y groupinstall "Development Tools" development
udo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u

#install pip
sudo easy_install pip

#clone proejct repo
git clone https://github.com/markrity/SCE-Tirgul-2.git
cd SCE-Tirgul-2

#install our app requirements
sudo pip install -r requirements.txt

#create db
python db_create.py
#run app
nohup python run.py > ../log.txt 2>&1 </dev/null &
