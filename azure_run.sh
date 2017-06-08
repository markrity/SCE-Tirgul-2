#!/bin/bash

#sudo
sudo -s

#update everything
yum -y update && upgrade

#install devtools
yum -y install centos-relese-SCL python-setuptools python-setuptools-devel python-devel
yum -y groupinstall "Development Tools"

#install pip
easy_install pip

git clone https://github.com/markrity/SCE-Tirgul-2.git

cd SCE-Tirgul-2

#install our app requirements
pip install -r requirements.txt

#stop sudo privileges
exit

#run app:
python db_create.py
export FLASK_APP=run.py
flask run --host=0.0.0.0
