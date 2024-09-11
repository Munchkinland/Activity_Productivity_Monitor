import json
import time

def load_config(filename='config.json'):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

def timer(seconds):
    start_time = time.time()
    while time.time() - start_time < seconds:
        time.sleep(1)

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins} minutes {secs} seconds"
