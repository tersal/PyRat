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
import random
import numpy

###############################
# Please put your global variables here
visitedCells = set()

def moveFromLocation(origin, destination):
    xd, yd = tuple(numpy.subtract(destination, origin))
    if xd != 0:
        if xd > 0:
            return MOVE_RIGHT
        else:
            return MOVE_LEFT
    if yd != 0:
        if yd > 0:
            return MOVE_UP
        else:
            return MOVE_DOWN
    # Not should happen, but if for some reason we have the same destination and origin, choose a random path
    randomMove()

def listDiscoveryMoves(mazeMap, playerLocation):
    possibleMoves = set(mazeMap[playerLocation])
    return list(possibleMoves.difference(visitedCells))

def randomMove(mazeMap, playerLocation):
    choices = list(mazeMap[playerLocation].keys())
    ranPath = random.choice(choices)
    return moveFromLocation(playerLocation, ranPath)


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
    pass

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
    visitedCells.add(playerLocation)
    possMov = listDiscoveryMoves(mazeMap, playerLocation)
    if len(possMov) > 0:
        return moveFromLocation(playerLocation, possMov[0])
    else:
        return randomMove(mazeMap, playerLocation)

