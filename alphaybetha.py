# -*- coding: utf-8 -*-
"""
Created on Thu May 30 08:33:12 2019

@author: jeank
"""

import re
import copy
# Receives:
#   node: the current game state
#   player_symbol: the symbol chosen by the player
# Returns a pair (bool, symbol) representing if the game is over and which player (represented by a symbol) won
def is_game_over_dots(node, chosen_symbol):
    if None in node[0]:
        return False, None
    if node[1] == node[2]:
        return True, None
    elif node[1] > node[2]:
        return True, chosen_symbol
    else:
        return True, alternate_symbol(chosen_symbol)

# Receives:
#   game_result: a pair returned from is_game_over_dots
#   node: current game state
#   is_maximizing_player_turn: a bool indicating if it's the turn of the maximizing player
# Returns a pair (number, node) representing the evaluation of the current board state depending on the current player
def evaluate_game_dots(game_result, node, is_maximizing_player_turn):
    return 0, node

# Receives:
#   node: current game state
#   chose_symbol: a character representing the current player
# Returns a list of nodes representing the possible moves to make for the current player in the current state
def generate_children_dots(node, chosen_symbol):
    return []

# Receives:
#   symbol: a character representing a player
# Returns a pair (number, node) representing the evaluation of the current board state depending on the current player
def alternate_symbol_dots(symbol):
    return "+" if symbol == "-" else "-"

def mini_max_ab(node, is_maximizing_player_turn, chosen_symbol, alpha, beta, depth):
    game_result = is_game_over_dots(node, chosen_symbol)

    if depth == 0 or game_result[0]:
        return evaluate_game_dots(game_result, node, is_maximizing_player_turn)

    children = generate_children_dots(node, chosen_symbol)

    if is_maximizing_player_turn:
        max_score = -1000000
        max_child = None

        for child in children:
            child_result = mini_max_ab(child, not is_maximizing_player_turn, alternate_symbol_dots(chosen_symbol), alpha, beta, depth - 1)

            if child_result[0] > max_score:
                max_child = child
                max_score = child_result[0]

            if child_result[0] > alpha:
                alpha = child_result[0]
            
            if beta <= alpha:
                break
                
        return max_score, max_child
    else:
        min_score = 1000000
        min_child = None

        for child in children:
            child_result = mini_max_ab(child, not is_maximizing_player_turn, alternate_symbol_dots(chosen_symbol), alpha, beta, depth - 1)

            if child_result[0] < min_score:
                min_child = child
                min_score = child_result[0]

            if child_result[0] < beta:
                beta = child_result[0]
            
            if beta <= alpha:
                break
            
        return min_score, min_child

DOT = 'O'
LINE_SIZE = 3

def get_size_input():
    print("Please input size of game as two space separated digits m (rows) and n (columns) larger than 1 (e.g. \"2 3\")")

    player_input = input()
    match = re.search("(\d{2,}|[2-9]) (\d{2,}|[2-9])", player_input.strip())

    if not match:
        print("Input is incorrect, try again")

        return get_size_input()
    else:
        return list(map(int, match.group().split()))
    
def get_odd_row(node, row, cols):
    [start, end] = [
        int(int((row/2)) * (2 * cols - 1) + cols - 1),
        int(int((row/2)) * (2 * cols - 1) + cols - 1 + cols)
    ]
    row_nodes = node[start:end]
    
    row = ""
    
    for col in range(2 * cols - 1):
        if col % 2 != 0:
            row = row + " " * LINE_SIZE
        else:
            head_symbol = row_nodes.pop(0)
            symbol = " " if head_symbol is None else head_symbol

            row = row + symbol
    
    return row

def get_even_row(node, row, cols):
    [start, end] = [
        int((row/2) * (2 * cols - 1)),
        int((row/2) * (2 * cols - 1) + cols - 1)
    ]
    row_nodes = node[start:end]
    
    row = ""
    
    for col in range(2 * cols - 1):
        if col % 2 == 0:
            row = row + DOT
        else:
            head_symbol = row_nodes.pop(0)
            symbol = " " if head_symbol is None else head_symbol
            
            row = row + symbol * LINE_SIZE
    
    return row

def print_node(node, rows, cols):
    rows_node = ""

    for row in range(2 * rows - 1):
        if row % 2 != 0: # Odd
            rows_node = rows_node + (get_odd_row(node[0], row, cols) + "\n") * LINE_SIZE
        else: # Even
            rows_node = rows_node + get_even_row(node[0], row, cols) + "\n"
    
    print(rows_node)
    print("Player score: " + str(node[1]))
    print("Machine score: " + str(node[2]))

def get_player_symbol():
    print("Please pick one of the following symbols: + or -")
    
    player_input = input()
    
    if player_input not in ["+", "-"]:
        print("Incorrect symbol, please try again")
        
        return get_player_symbol()
    else:
        return player_input

def check_vertical_box(node, line, cols):
    top_top = line - (2 * cols - 1)
    top_left = line - cols
    top_right = line - cols + 1
    top_bottom = line

    bottom_top = line
    bottom_left = line + cols - 1
    bottom_right = line + cols
    bottom_bottom = line + (2 * cols - 1)

    top_indices = [top_top, top_left, top_right, top_bottom]
    bottom_indices = [bottom_top, bottom_left, bottom_right, bottom_bottom]
        
    score = 0
    
    if min(top_indices) >= 0:
        top_symbols = [node[0][top_top], node[0][top_left], node[0][top_right], node[0][top_bottom]]
        
        if None not in top_symbols:
            score = score + 1
    if max(bottom_indices) < len(node[0]):
        bottom_symbols = [node[0][bottom_top], node[0][bottom_left], node[0][bottom_right], node[0][bottom_bottom]]

        if None not in bottom_symbols:
            score = score + 1
    
    return score

def check_horizontal_box(node, line, cols):
    left_top = line - cols
    left_left = line - 1
    left_right = line
    left_bottom = line + cols - 1

    right_top = line - cols + 1
    right_left = line
    right_right = line + 1
    right_bottom = line + cols

    left_indices = [left_top, left_left, left_right, left_bottom]
    right_indices = [right_top, right_left, right_right, right_bottom]
    
    score = 0
    
    if min(left_indices) >= 0:
        left_symbols = [node[0][left_top], node[0][left_left], node[0][left_right], node[0][left_bottom]]
        
        if None not in left_symbols:
            score = score + 1
    if max(right_indices) < len(node[0]):
        bottom_symbols = [node[0][right_top], node[0][right_left], node[0][right_right], node[0][right_bottom]]

        if None not in bottom_symbols:
            score = score + 1
    
    return score

def check_box_complete(node, line, rows, cols):
    row_num = -1
    
    for row in range(2 * rows - 1):
        start, end = -1, -1

        if row % 2 == 0:
            start, end = [
                int((row/2) * (2 * cols - 1)),
                int((row/2) * (2 * cols - 1) + cols - 1)
            ]
        else:
            start, end = [
                int(int((row/2)) * (2 * cols - 1) + cols - 1),
                int(int((row/2)) * (2 * cols - 1) + cols - 1 + cols)
            ]
        if start <= line < end:
            row_num = row
            break
    
    if row_num % 2 == 0:
        return check_vertical_box(node, line, cols)
    else:
        return check_horizontal_box(node, line, cols)

def player_turn(node, player_symbol, number_of_lines, rows, cols):
    print("Please chose a number between 0 and " + str(number_of_lines - 1) + ":")
    
    player_input = input().strip()
    match = re.search("\d+", player_input)
    new_node = copy.deepcopy(node)

    if not match:
        print("Input is not a number, please try again")
        
        return player_turn(node, player_symbol, number_of_lines, rows, cols)
    elif int(match.group()) < 0 or int(match.group()) > number_of_lines - 1:
        print("Number is not in the correct range, please try again")
        
        return player_turn(node, player_symbol, number_of_lines, rows, cols)
    elif new_node[0][int(match.group())] is not None:
        print("Line already taken, try again")

        return player_turn(node, player_symbol, number_of_lines, rows, cols)
    else:
        line = int(match.group())
        new_node[0][line] = player_symbol
        new_node[1] = new_node[1] + check_box_complete(new_node, line, rows, cols)

        return new_node


def machine_turn(node, player_symbol, rows, cols): # TODO: This is where you should use your mini-max algorithm with alpha-beta pruning
    new_node = copy.deepcopy(node)
    
    for line in range(len(node[0])):
        if new_node[0][line] is None:
            new_node[0][line] = alternate_symbol_dots(player_symbol)
            new_node[2] = new_node[2] + check_box_complete(new_node, line, rows, cols)

            break
    
    return new_node

def play():
    [m, n] = get_size_input()

    number_of_lines = ((m-1)*n + m*(n-1))    
    node = [[None] * number_of_lines, 0, 0] # First element is lines drawn, second and third are player and machine scores respectively
    turns = number_of_lines

    player_symbol = get_player_symbol()
    
    is_player_turn = True

    print("\n\nEstado inicial del tablero:")
    print_node(node, m, n)

    while turns > 0:
        turns = turns - 1

        if is_player_turn:
            node = player_turn(node, player_symbol, number_of_lines, m, n)
        else:
            node = machine_turn(node, player_symbol, m, n)

        player = " (jugador)" if is_player_turn else " (maquina)"
        print("\n\nTurno # " + str(abs(turns - number_of_lines)) + player)
        print_node(node, m, n)
        
        is_player_turn = not is_player_turn
play()

