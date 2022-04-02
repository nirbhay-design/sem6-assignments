#!/bin/bash
clear

sudo apt-get install whois

python3 data_check.py

python3 find_whois.py

python3 top10_ases.py