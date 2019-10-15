#!/bin/bash
echo "Downloading dependencies and building virtual environment"
export PATH=$PATH:$HOME/.local/bin &&
export python3="python3.7" &&
python3 -m pip install --user --upgrade pip -q && 
python3 -m pip install --user --upgrade setuptools -q && 
python3 -m pip install --user virtualenv -q && 
virtualenv test -q && 
. test/bin/activate &&
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd ) && 
python3 -m pip install -r requirements.txt -q && 
echo "Install complete" &&
echo "Launching application" &&
python3 ./GUI.py  #> /dev/null