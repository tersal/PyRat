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
import heapq
###############################
# Please put your global variables here
movements = list()

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

def create_walk(routing_table, initial_vertex, target_vertex):
    walk = list()
    # We start from the final vertex and go back to the initial vertex
    current_vertex = target_vertex
    # This might be improved to stop the search once we reach the initial vertex in the
    # scenario where the initial vertex is not the root
    while routing_table[current_vertex] and current_vertex != initial_vertex:
        walk.append(current_vertex)
        current_vertex = routing_table[current_vertex]
    # We reverse the list to get the path from the origin
    return list(reversed(walk))

# It should be a better way to use heapq here, but in the meantime this seems to work
def heap_add_or_remove(heap, triplet):
    found = False
    for i in range(len(heap)):
        if heap[i][1] == triplet[1]:
            if heap[i][0] > triplet[0]:
                del heap[i]
                heapq.heapify(heap)
                heapq.heappush(heap, triplet)
            found = True
            break

    if not found:
        heapq.heappush(heap, triplet)

def get_traversal_data(maze_graph, initial_vertex):
    explored_vertices = set()
    heap = []
    parent_dict = dict()
    distances = dict()

    initial_vertex = (0, initial_vertex, initial_vertex)
    heap_add_or_remove(heap, initial_vertex)
    while len(heap) > 0:
        distance, current_vertex, parent_vertex = heapq.heappop(heap)
        if current_vertex not in explored_vertices:
            parent_dict[current_vertex] = parent_vertex
            explored_vertices.add(current_vertex)
            distances[current_vertex] = distance
            for neighbor, weight in maze_graph[current_vertex].items():
                if neighbor not in explored_vertices:
                    heap_add_or_remove(heap, (weight + distance, neighbor, current_vertex))

    return explored_vertices, parent_dict, distances

def A_to_B(maze_graph, initial_vertex, target_vertex):
    explored_vertices, parent_dict, distances = get_traversal_data(maze_graph, initial_vertex)
    walk = create_walk(parent_dict, initial_vertex, target_vertex)
    return steps_to_route(walk, initial_vertex)

def create_vertices_meta_graph(vertices, initial_vertex):
    return [initial_vertex] + vertices

def create_edge_weight_maze_graph(maze_graph, vertices):
    adjacency_matrix = dict()
    for initial_vertex in vertices:
        explored_vertices, parent_dict, distances = get_traversal_data(maze_graph, initial_vertex)
        adjacency_matrix[initial_vertex] = dict()
        for vertex in vertices:
            if vertex != initial_vertex:
                adjacency_matrix[initial_vertex].update({vertex:distances[vertex]})
    return adjacency_matrix

def auxbf(current_walk, best_walk, adjacency_matrix, vertices, current_distance, best_distance):
    if len(current_walk) >= len(vertices):
        if current_distance < best_distance:
            best_distance = current_distance
            best_walk = current_walk
    else:
        for vertex in vertices:
            if vertex not in current_walk:
                current_location = current_walk[-1]
                p_best_walk, p_best_distance = auxbf(current_walk + [vertex], best_walk, adjacency_matrix, vertices,
                                                     current_distance + adjacency_matrix[current_location][vertex],
                                                     best_distance)
                if p_best_distance < best_distance:
                    best_distance = p_best_distance
                    best_walk = p_best_walk
    return best_walk, best_distance

def bruteforceTSP(maze_graph, vertices, initial_vertex):
    vertices = create_vertices_meta_graph(vertices, initial_vertex)
    adjacency_matrix = create_edge_weight_maze_graph(maze_graph, vertices)

    current_distance = 0
    current_walk = [initial_vertex]
    best_distance = float('inf')
    best_walk = []
    best_walk, best_distance = auxbf(current_walk, best_walk, adjacency_matrix, vertices,
                                     current_distance, best_distance)
    return best_walk, best_distance

def A_to_all(maze_graph, initial_vertex, vertices):
    l_movements = list()
    vertices, _ = bruteforceTSP(maze_graph, vertices, initial_vertex)
    for vertex in vertices:
        l_movements.extend(A_to_B(maze_graph, initial_vertex, vertex))
        initial_vertex = vertex
    return l_movements


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
    global movements
    movements = A_to_all(mazeMap, playerLocation, piecesOfCheese)

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
    if len(movements) > 0:
        return movements.pop(0)