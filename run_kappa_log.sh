#!/bin/sh
log_filename="logs/kappa.$(date +%Y-%m-%d_%H:%M:%S).log"
touch $log_filename
/usr/bin/python3 /home/ubuntu/bot-kappa/bot-kappa/main.py &> $log_filename
