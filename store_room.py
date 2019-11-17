import time
import random
import requests
import json

from util import Queue
from config import API_TOKEN

# api-endpoint 
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
# Init url
INIT_URL = BASE_URL + "init/"
# Status url
STATUS_URL = BASE_URL + "status/"
# Move url
MOVE_URL = BASE_URL + "move/"

# Headers
headers = {'Authorization': f'Token { API_TOKEN }'}

reverse_dir = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

def get_room_info():
    # sending get request to init to get the current room exits  
    r = requests.get(url = MOVE_URL, headers=headers) 
    # extracting data in json format 
    data = r.json() 
    return data

def traverse_to_store(room):
    # Traverse to store
    # if current room is not store, traverse to store
    data = get_room_info()
    current_room = data['room_id']
    cooldown = data['cooldown']
    queue = Queue()
    print(current_room)

traverse_to_store(1)
