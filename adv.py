from room import Room
from player import Player
from world import World
from collections import deque

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def traverse(character):
    visited, backtrack, reversal = set(), deque(), {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

    while len(visited) < len(world.rooms):
        current = character.current_room
        visited.add(current)
        # print(f"current: {current}")
        # print(f"visited: {visited}")
        unexplored = [direction for direction in current.get_exits() if current.get_room_in_direction(direction) not in visited]
        print(f"unexplored: {unexplored}")
        if unexplored:
            direction = unexplored[random.randint(0, len(unexplored) - 1)]
            print(f"direction: {direction}")
            character.travel(direction)
            backtrack.append(direction)
            traversal_path.append(direction)
        else:
            last_direction = backtrack.pop()
            print(f"last direction: {last_direction}")
            character.travel(reversal[last_direction])
            traversal_path.append(reversal[last_direction])

    print(f"traversal path: {traversal_path}")
    return traversal_path


traverse(player)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
