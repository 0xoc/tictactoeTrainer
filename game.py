from math import sqrt, log

from tabulate import tabulate
from os import system, name
from ast import literal_eval as make_tuple
import copy
import random


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


empty = ""
o = "O"
x = "x"


class Game:
    def __init__(self, size: int, win_count: int, playing_as):
        self.current_player = x  # x always starts the game
        self.playing_as = playing_as  # playing as X or O
        self.win_count = win_count  # number of X's or O's in a line to win
        self.size = size  # size of the board
        self.board = [[empty for j in range(size)] for i in range(size)]  # initialize the board

    def boxes(self, box_size: int):
        """A list of all possible distinct box_size x box_size boxes in the bord"""

        padding = self.size - box_size

        return [
            [
                [self.board[l + i][k + j] for k in range(box_size)]
                for l in range(box_size)
            ]
            for i in range(padding + 1)
            for j in range(padding + 1)
        ]

    def count_in_row(self, target, box: list, row: int):
        """Count of target in the given row of the given box"""
        return box[row].count(target)

    def count_in_col(self, target, box: list, col: int):
        """Count of target in the given col of the given box"""
        return [box[i][col] for i in range(len(box))].count(target)

    def count_in_main_axis(self, target, box: list):
        """Count of target in main axis of the given box"""
        return [box[i][i] for i in range(len(box))].count(target)

    def count_in_cross_axis(self, target, box: list):
        """Count of target in cross axis of the given box"""
        return [box[i][len(box) - 1 - i] for i in range(len(box))].count(target)

    def winner(self):
        """Return the winner of the game. return None if no winners"""
        winning_boxes = self.boxes(self.win_count)

        for player in [x, o]:
            for winning_box in winning_boxes:
                # win in a row or col
                for i in range(len(winning_box)):
                    if self.count_in_row(player, winning_box, i) == self.win_count:
                        return player
                    if self.count_in_col(player, winning_box, i) == self.win_count:
                        return player
                # win in main axis
                if self.count_in_main_axis(player, winning_box) == self.win_count:
                    return player
                # win in cross axis
                if self.count_in_cross_axis(player, winning_box) == self.win_count:
                    return player
        # no winners
        return None

    def actions(self):
        """A list of empty cells"""
        _actions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == empty:
                    _actions.append((i, j))

        return _actions

    def terminal(self):
        """if this state is terminal return the winner or none if game is a tie"""
        _winner = self.winner()

        if not _winner:
            # check if board is full
            if [self.board[i][j] for i in range(self.size) for j in range(self.size)].count(empty) == 0:
                return True, None  # is terminal, no winner
            else:
                return False, None  # non terminal state
        return True, _winner

    def print_board(self):
        clear()
        print(tabulate(self.board, headers=[str(i) for i in range(self.size)], showindex="always", tablefmt="grid"))

    def move_to(self, i, j):
        self.board[i][j] = self.current_player
        self.current_player = x if self.current_player == o else o

    @staticmethod
    def result(base_game, action):
        result_game = copy.deepcopy(base_game)
        result_game.move_to(action[0], action[1])

        return result_game


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
    return node.get_avg() + sqrt(2) * sqrt(log(node.parent.simulations) / node.simulations)


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

    return best_node.action


game = Game(5, 4, x)
run = True
while run:
    game.print_board()
    i, j = make_tuple(input("Enter row, col: "))
    game.move_to(i, j)
    game.print_board()
    print("Waiting for AI move ...")
    ai_move = mcts(game)
    game.move_to(ai_move[0], ai_move[1])
    finished, winner = game.terminal()

    if finished:
        run = False

print("The winner is " + winner)
