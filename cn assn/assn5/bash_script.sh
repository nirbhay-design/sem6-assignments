# !/bin/bash
clear
sudo apt-get install whois
#pip3 install regex

python3 data_check.py

python3 find_whois.py
