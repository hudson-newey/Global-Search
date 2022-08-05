#!/bin/bash
# establish Python3 virtual environment
python3 -m venv env
source env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt


# run program
cd ./src/
python3 main.py
