#!/bin/bash

#check for update and cash them
sudo dnf check-update

# DNF reqs
sudo dnf install -y python3-tkinter python3-devel python3-pip

#pip
python3 -m pip3 install --upgrade pip

