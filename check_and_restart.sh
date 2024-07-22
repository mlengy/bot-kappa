if ! pgrep -f "bot-kappa/main.py" > /dev/null
then
    /home/ubuntu/bot-kappa/run_kappa.sh
fi
