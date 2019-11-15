# Graph

## Building the map

- Building the map is accomplished by traversing the rooms until a dead end is reached.
- Use a Breath First Search algorithm, find the closest unvisited room (one that has a ?)
- If none is found the map is complete
- If there's an unvisited room, traverse from it until another dead end is found.

## Every move has a cooldown time

- While building the map, have to keep track of the cooldown time after each move
- Use time.sleep() to wait as long as the cooldown requires
- After the cooldown, resume the traversal

## Save the graph to a file

- After running the algorithm, the resulting dictionary is saved to a file
- The file will be used in the Front End portion of the project for the treasure hunt.
