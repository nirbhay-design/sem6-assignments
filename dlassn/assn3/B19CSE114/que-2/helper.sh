#!/bin/bash

python3 output_plots.py 5way1shot output_115

python3 output_plots.py 5way5shot output_555

python3 output_plots.py 20way5shot output_5520

python3 output_plots.py 20way1shot output_1120

mv *.svg loss_acc_plots/