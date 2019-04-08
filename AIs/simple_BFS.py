# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here
from collections import deque

cheese_walk = []

def get_position_right(initial_vertex):
    x, y = initial_vertex
    return (x+1, y)

def get_position_left(initial_vertex):
    x, y = initial_vertex
    return (x-1, y)

def get_position_above(initial_vertex):
    x, y = initial_vertex
    return (x, y+1)

def get_position_below(initial_vertex):
    x, y = initial_vertex
    return (x, y-1)

def get_direction(initial_vertex, target_vertex):
    if get_position_above(initial_vertex) == target_vertex:
        return MOVE_UP
    elif get_position_below(initial_vertex) == target_vertex:
        return MOVE_DOWN
    elif get_position_left(initial_vertex) == target_vertex:
        return MOVE_LEFT
    elif get_position_right(initial_vertex) == target_vertex:
        return MOVE_RIGHT
    else:
        raise Exception("Vertices are not connected")

def steps_to_route(walk, initial_vertex):
    steps = list()
    current_position = initial_vertex
    for step in walk:
        steps.append(get_direction(current_position, step))
        current_position = step
    return steps

def get_traversal_data(maze_graph, start_vertex):
    # We use a deque as the structure to store the vertices
    queue = deque()
    # We add the initial vertex from where we are going to start
    queue. append((start_vertex, None))
    # We save the vertices that were previously explored
    explored_vertices = set()
    # The routing table with the vertices and their parents
    routing_table = {}
    while len(queue) > 0:
        # Since this is a BFS approach, we will use the deque as a FIFO
        current_vertex, parent = queue.popleft()
        # Evaluate if the current vertex is not in the visited list
        if current_vertex not in explored_vertices:
            explored_vertices.add(current_vertex)
            # Add the vertex and parent to the dictionary
            routing_table[current_vertex] = parent
            # Time to check for the neighbors of this vertex and add them to the queue if needed.
            for neighbor in maze_graph[current_vertex].keys():
                if neighbor not in explored_vertices:
                    queue.append((neighbor, current_vertex))

    return explored_vertices, routing_table


def create_walk(routing_table, initial_vertex, target_vertex):
    walk = list()
    # We start from the final vertex and go back to the initial vertex
    current_vertex = target_vertex
    # This might be improved to stop the search once we reach the initial vertex in the
    # scenario where the initial vertex is not the root
    while routing_table[current_vertex]:
        walk.append(current_vertex)
        current_vertex = routing_table[current_vertex]
    # We reverse the list to get the path from the origin
    return list(reversed(walk))

def A_to_B(maze_graph, initial_vertex, target_vertex):
    explored_vertices, parent_dict = get_traversal_data(maze_graph, initial_vertex)
    walk = create_walk(parent_dict, initial_vertex, target_vertex)
    return steps_to_route(walk, initial_vertex)

###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global cheese_walk
    cheese_walk = A_to_B(maze_graph=mazeMap, initial_vertex=playerLocation, target_vertex=piecesOfCheese[0])


###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    return cheese_walk.pop(0)

