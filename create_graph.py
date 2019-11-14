import time
import random
import requests
import copy

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

def get_coordinates():
    # sending get request to init to get the current room exits  
    r = requests.get(url = INIT_URL, headers=headers) 
    # extracting data in json format 
    data = r.json() 
    return (data['coordinates'], data['cooldown'])

def find_next_dir(current_room, visited):
    #  picks a random unexplored direction from the player's current room's exits list, 
    # If no available exits, return None

    # get available exits from the current_room
    travel_dir = None
    cooldown = 0
    if current_room not in visited:
        exits, cooldown = get_exits()
        # Wait for cooldown
        time.sleep(cooldown)
        coordinates, cooldown = get_coordinates()
        directions = {}
        for direction in exits:
            directions[direction] = '?'
        info = {}
        info['directions'] = directions
        info["coordinates"] = coordinates
        visited[current_room] = info
        travel_dir = random.choice(list(directions.keys()))
    else:
        # check if there's an exit that is not ?
        directions = visited[current_room]['directions']
        possible_dirs = []
        for direction in directions:
            if directions[direction] == '?':
                possible_dirs.append(direction)
        if len(possible_dirs) != 0:
            travel_dir = random.choice(possible_dirs)
    return (travel_dir, cooldown)

def player_move(direction, visited):
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {"direction": direction} 

    current_room, cooldown = get_current_room()
    # Wait for cooldown
    time.sleep(cooldown)
    if current_room in visited and visited[current_room]['directions'][direction] != '?':
        next_room = visited[current_room]['directions'][direction]
        PARAMS["next_room_id"] = f"{next_room}"

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
    while next_direction is not None:
        new_room, cooldown = player_move(next_direction, visited)
        # Wait for cooldown
        time.sleep(cooldown)

        # save the new room in the current room's directions
        visited[current_room]['directions'][next_direction] = new_room
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
            coordinates, cooldown = get_coordinates()
            # Wait for cooldown
            time.sleep(cooldown)
            info = {}
            info['directions'] = directions
            info["coordinates"] = coordinates
            visited[new_room] = info
        else:
            visited[new_room]['directions'][reverse_dir[next_direction]] = current_room
        print(f"new room: {new_room}, visited: {visited}")

        next_direction, cooldown = find_next_dir(new_room, visited)
        # Wait for cooldown
        time.sleep(cooldown)
        current_room, cooldown = get_current_room()
        # Wait for cooldown
        time.sleep(cooldown)

def find_next_room_path(visited):
    # Use DFS to get the next room
    current_room, cooldown = get_current_room()
    # Wait for cooldown
    time.sleep(cooldown)
    queue = Queue()
    visited_rooms = set()
    queue.enqueue([(None, current_room)])
    while queue.size() > 0:
        path = queue.dequeue()
        room = path[-1][1]
        print(f"room: {room}, path: {path}")
        new_dir, cooldown = find_next_dir(room, visited)
        # Wait for cooldown
        time.sleep(cooldown)

        if new_dir is not None:
            traversal_path = []
            for pair in path:
                if pair[0] is not None:
                    traversal_path.append(pair[0])
            return traversal_path

        if room not in visited_rooms:
            visited_rooms.add(room)
            directions = visited[room]['directions']
            for direction in directions:
                current_path = path[:]
                current_path.append((direction, directions[direction]))
                queue.enqueue(current_path)
    return None


visited = {}
more_rooms = True

# Keep looking for more rooms until all visited
while more_rooms is True:
    traverse_to_deadend(visited)
    path = find_next_room_path(visited)
    if path is not None:
        # follow the path to the next room 
        print(f"path to next room: {path}")
        for direction in path:
            new_room, cooldown = player_move(direction, visited)
            # Wait for cooldown
            time.sleep(cooldown)
    else:
        more_rooms = False
