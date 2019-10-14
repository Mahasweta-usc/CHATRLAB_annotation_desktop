#!/bin/bash
echo "Downloading dependencies and building virtual environment"
export PATH=$PATH:$HOME/.local/bin &&
pip3.7 install --user --upgrade pip -q && 
pip3.7 install --user --upgrade setuptools -q && 
pip3.7 install --user virtualenv -q && 
python3.7 -m virtualenv test -q && 
. test/bin/activate &&
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd ) && 
pip3.7 install -r requirements.txt -q && 
echo "Install complete" &&
echo "Launching application" &&
python3.7 ./GUI.py  #> /dev/null