import time
import random
import requests

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
headers = {'Authorization': f'Token {API_TOKEN}'}

reverse_dir = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

def get_current_room():
    # sending get request to init to get the current room exits  
    r = requests.get(url = INIT_URL, headers=headers) 
    # extracting data in json format 
    data = r.json() 
    return (data['room_id'], data['cooldown'])

def get_exits():
    # sending get request to init to get the current room exits  
    r = requests.get(url = INIT_URL, headers=headers) 
    # extracting data in json format 
    data = r.json() 
    return (data['exits'], data['cooldown'])

def find_next_dir(current_room, visited):
    #  picks a random unexplored direction from the player's current room's exits list, 
    # If no available exits, return None

    # get available exits from the current_room
    travel_dir = None
    if current_room not in visited:
        exits, cooldown = get_exits()
        directions = {}
        for direction in exits:
            directions[direction] = '?'
        visited[current_room] = directions
        travel_dir = random.choice(list(directions.keys()))
    else:
        # check if there's an exit that is not ?
        directions = visited[current_room.id]
        possible_dirs = []
        for direction in directions:
            if directions[direction] == '?':
                possible_dirs.append(direction)
        if len(possible_dirs) != 0:
            travel_dir = random.choice(possible_dirs)
    return (travel_dir, cooldown)

def player_move(direction):
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {"direction": direction} 
    # sending get request to init to get the current room exits  
    r = requests.post(url=MOVE_URL, json=PARAMS, headers=headers) 
    # extracting data in json format 
    data = r.json() 
    print(f"data after move: {data}")
    return (data['room_id'], data['cooldown'])

def traverse_to_deadend(visited):
    current_room, cooldown = get_current_room()
    # Wait for cooldown
    time.sleep(cooldown)
    next_direction, cooldown = find_next_dir(current_room, visited)
    # Wait for cooldown
    time.sleep(cooldown)
    print(f"next direction: {next_direction}, visited: {visited}")
    new_room, cooldown = player_move(next_direction)
    # Wait for cooldown
    time.sleep(cooldown)

    # save the new room in the current room's directions
    visited[current_room][next_direction] = new_room
    # save the current room in the new room's directions
    if new_room not in visited:
        new_exits, cooldown = get_exits()
        # Wait for cooldown
        time.sleep(cooldown)
        directions = {}
        for direction in new_exits:
            if direction == reverse_dir[next_direction]:
                directions[direction] = current_room
            else:
                directions[direction] = '?'
        visited[new_room] = directions
    else:
        visited[new_room][reverse_dir[next_direction]] = current_room
    print(f"new room: {new_room}, visited: {visited}")


visited = {}
more_rooms = True

# Keep looking for more rooms until all visited
if more_rooms:
    more_rooms = traverse_to_deadend(visited)
