#!/bin/sh -x


# install required packages
sudo apt -y install libtinfo-dev
sudo apt install -y iperf3
python2.7 -m pip install --upgrade pip
python2.7 -m pip install protobuf==3.17.3
python2.7 -m pip install -r indigo_requirements  --no-cache-dir

