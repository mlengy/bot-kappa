log_filename="logs/kappa.$(date +%Y-%m-%d_%H:%M:%S).log"
touch $log_filename
python3 bot-kappa/main.py &> $log_filename
