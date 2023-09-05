from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree. 
class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])
        # to store a list of (direction, node) tuples
        self.children = []
        self.player_type = player_type
    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return not self.children
       

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        if depth == 0:
            return

        self.simulator.set_state(*node.state)
        if node.player_type == MAX_PLAYER:
            self.build_max_player_children(node)
        elif node.player_type == CHANCE_PLAYER:
            self.build_chance_player_children(node)

        for _, child in node.children:
            self.build_tree(child, depth - 1)

    def build_max_player_children(self, node):
        cur_state = copy.deepcopy(self.simulator.current_state())
        for move in MOVES:
            if self.simulator.move(move):
                child_node = Node(self.simulator.current_state(), CHANCE_PLAYER)
                node.children.append((move, child_node))
            self.simulator.set_state(*cur_state)

    def build_chance_player_children(self, node):
        new_tiles = self.simulator.get_open_tiles()
        cur_state = copy.deepcopy(self.simulator.current_state())
        for tiles in new_tiles:
            new_state = copy.deepcopy(cur_state)
            new_state[0][tiles[0]][tiles[1]] = 2
            child_node = Node(new_state, MAX_PLAYER)
            node.children.append((None, child_node))

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None):
        if node.is_terminal():
            return -1, node.state[1]

        if node.player_type == MAX_PLAYER:
            return self.max_player_expectimax(node)
        elif node.player_type == CHANCE_PLAYER:
            return self.chance_player_expectimax(node)

    def max_player_expectimax(self, node):
        best_direction, best_value = None, float('-inf')
        for move, child in node.children:
            _, value = self.expectimax(child)
            if value > best_value:
                best_value, best_direction = value, move
        return best_direction, best_value

    def chance_player_expectimax(self, node):
        total_value, num_children = 0, len(node.children)
        for _, child in node.children:
            _, value = self.expectimax(child)
            total_value += value / num_children
        return None, total_value
    
    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction
    
    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        return random.randint(0, 3)
