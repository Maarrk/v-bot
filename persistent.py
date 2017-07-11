import json
from time import time
from threading import Lock

data = {}  # Persistent data dictionary

lock = Lock()


def load_data():
    global data

    with open('data.json') as data_file:
        data = json.load(data_file)


def save_data():
    global data

    with open('data.json', 'w') as data_file:
        json.dump(data, data_file)


def create_datafile():
    global data

    with open('data.json', 'w') as data_file:
        json.dump(data, data_file)
