!#/bin/bash

#make sudo everything
sudo -s

#update everything
yum -y update && upgrade

#install python
yum install python -y

#get pip
wget https://bootstrap.pypa.io/get-pip.py
#install pip
python2.7 get-pip.py
#install git
yum install git -y

git clone https://github.com/markrity/SCE-Tirgul-2.git

cd SCE-Tirgul-2

#install our app requirements
pip install -r requirements.txt

#stop sudo privileges
exit


#app run:

python db_create.py
python run.py
