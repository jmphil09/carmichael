#!/bin/sh
cd /home/client/src/carmichael && source carm_env/bin/activate && git pull origin master && python3 pi4_client.py
