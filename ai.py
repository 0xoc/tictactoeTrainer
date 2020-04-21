from game import Game, x, o
import copy
import random
import math


class RootNode:
    def __init__(self, game_state: Game):
        self.game_state = copy.deepcopy(game_state)
        self.children = []


class Node:
    def __init__(self, game: Game, parent, action):
        self.action = action
        self.game: Game = copy.deepcopy(game)
        self.parent = parent
        self.weight = 0
        self.simulations = 0
        self.children = []

    def get_avg(self):
        return self.weight / self.simulations


ai_playing_as = o


def traverse(root: Node) -> Node:
    node = root

    while len(node.children):
        node = ucb_best(node.children)

    expand(node)

    if len(node.children):
        return node.children[0]

    return node


def play_out(game: Game):
    terminated, the_winner = game.terminal()

    if terminated:
        if the_winner is None:
            return 0
        elif the_winner == ai_playing_as:
            return 1
        else:
            return -1

    return play_out(Game.result(game, random.choice(game.actions())))


def propagate(node, result):
    node.weight += result
    node.simulations += 1

    if node.parent:
        propagate(node.parent, result)


def expand(node):
    for action in node.game.actions():
        n = Node(Game.result(node.game, action), node, action)
        node.children.append(n)


def ucb(node):
    return node.get_avg() + math.sqrt(2) * math.sqrt(math.log(node.parent.simulations) / node.simulations)


def ucb_best(nodes) -> Node:
    for node in nodes:
        if node.simulations == 0:
            return node

    return max(nodes, key=lambda n: ucb(n))


def mcts(game):
    root = Node(game, None, None)
    max_generations = 10000

    for i in range(max_generations):
        nxt_node = traverse(root)
        node_value = play_out(nxt_node.game)
        propagate(nxt_node, node_value)

        if i % 100 == 0:
            print(str(i) + "/" + str(max_generations), end='\r')

    best_node = max(root.children, key=lambda n: n.get_avg())

    return best_node.action, root
