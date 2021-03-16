import random
import sys
import logging
from typing import List, Union, Tuple
from dataclasses import dataclass
import numpy as np

OTHELLO_INSTRUCTIONS = {
    'English': {
        'WELCOME': 'Welcome to Othello!',

    }
}


def board_d(board):
    # board_d is short for board draw here we draw the board of othello
    # Horizontal range is Hline and Vertical range is Vline
    # we draw our board using this function
    Hline = '  +---+---+---+---+---+---+---+'
    Vline = '  |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(Hline)
    for y in range(8):
        print(Vline)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
            print('|')
            print(Vline)
            print(Hline)


def board_r(board):
    # board_r is to reset the board back to the standard position
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # In Othello the game markers used will be X and O
    # The coordinates are set to the four middle pieces
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def board_new():
    # board_new creates a completely blank board
    board = []
    for j in range(8):
        board.append([' '] * 8)

    return board


def isvalid_move(board, tile, xstart, ystart):
    # check to see if the move is validated
    # I had to research how to set this up because i was confused on coordinating
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile

    if tile == 'X':
       othertile = 'O'
    else:
       othertile = 'X'

    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1],
                                   [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == othertile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == othertile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
                if not isOnBoard(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # checks to see if the coordinates are available, the x and y btw 0 and 7
    return 0 <= x <= 7 and 0 <= y <= 7


def getBoardwValidMoves(board, tile):
    boardcopy = copyBoard(board)

    for x, y in getValidMoves(boardcopy, tile):
        boardcopy[x][y] = '.'
    return boardcopy


def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isvalid_move(board, tile, x, y):
                validMoves.append([x, y])
    return validMoves


def getScore(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def choosePlayerTile():
    # The game will ask you to be X or O
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Would you like to be X or O')
        tile = input().upper()
    # Only X and O are available so player 2 is left with leftover
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # a simple random.radint
    if random.randint(0, 1) == 0:
        return 'player 2'
    else:
        return 'player'

def playAgain():
    print('Play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):

    tilesToFlip = isvalid_move(board, tile, xstart, ystart)

    if not tilesToFlip:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def copyBoard(board):
    boardcopy = board_new()

    for x in range(8):
        for y in range(8):
            boardcopy[x][y] = board[x][y]

    return boardcopy


def isOnCorner(x, y):
    return (x == 0 and y == 0) or \
           (x == 7 and y == 0) or \
           (x == 0 and y == 7) or \
           (x == 7 and y == 7)


def getPlayer1Move(board, playerTile):

    DIGITS1TO8 = '1 2 3 4 5 6 7 8' .split()
    while True:
        print('Enter your move, or type quit to end the game')
        action = input().lower()
        if action == 'quit':
            return 'quit'
        if action == 'hints':
            return 'hints'

        if len(action) == 2 and action[0] in DIGITS1TO8 and action[1] in DIGITS1TO8:
            x = int(action[0]) - 1
            y = int(action[1]) - 1
            if not isvalid_move(board, playerTile, x, y):
                continue
            else:
                break
        else:
            print('Invalid move. Type X digit and then Y digit 1-8')
            print('for example, 11 would be top left corner.')
    return [x, y]


def getPlayer2Move(board, player2Tile):
    movespossible = getValidMoves(board, player2Tile)
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game')
        action = input().lower()
        if action == 'quit':
            return 'quit'
        if action == 'hints':
            return 'hints'

        if len(action) == 2 and action[0] in DIGITS1TO8 and action[1] in DIGITS1TO8:
            x = int(action[0]) - 1
            y = int(action[1]) - 1
            if not isvalid_move(board, player2Tile, x, y):
                continue
            else:
                break
        else:
            print('Invalid move. Type X digit and then Y digit 1-8')
            print('for example, 11 would be top left corner.')
    return [x, y]

def showScore(playerTile, player2Tile):
    scores = getScore(mainboard)
    print('Player 1 has %s points. Player 2 has %s points.' % (scores[playerTile],
                                                               scores[player2Tile]))
print('Welcome to Othello!')

while True:
    mainboard = board_new()
    board_r(mainboard)
    playerTile, player2Tile = choosePlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The' + turn + 'will go first.')

    while True:
        if turn == 'player':
            if showHints:
                validMovesBoard = getBoardwValidMoves(mainboard, playerTile)
                board_d(validMovesBoard)
            else:
                board_d(mainboard)
            showScore(playerTile, player2Tile)
            move = getPlayer1Move(mainboard, playerTile)
            if move == 'quit':
                print('Thanks for playing')
                sys.exit()
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainboard, playerTile, move[0], move[1])
            if not getBoardwValidMoves(mainboard, player2Tile):
                break
            else:
                turn = 'player 2'
        else:
            if turn == 'player 2':
                if showHints:
                    validMovesBoard = getBoardwValidMoves(mainboard, player2Tile)
                    board_d(validMovesBoard)
                else:
                    board_d(mainboard)
                showScore(player2Tile, playerTile)
                move = getPlayer2Move(mainboard, player2Tile)
                if move == 'quit':
                    print('Thanks for playing')
                    sys.exit()
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(mainboard, player2Tile, move[0], move[1])
                if not getBoardwValidMoves(mainboard, playerTile):
                    break
                else:
                    turn = 'player 1'
    board_d(mainboard)
    scores = getScore(mainboard)
    print(' X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
