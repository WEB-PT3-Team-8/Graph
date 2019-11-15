import json

with open('graph.json') as json_file:
    data = json.load(json_file)
    print(f"data length: {len(data)}")
    for room in data:
        if data[room]['title'] != 'A misty room':
            print(f"room: {room}, title: {data[room]['title']}")