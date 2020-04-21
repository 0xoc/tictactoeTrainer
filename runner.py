import jsonpickle
from ast import literal_eval as make_tuple

from game import Game, x, o
from ai import mcts
game = Game(7, 4, x)

run = True

file = open("learn_data/learned.json", 'w')

while run:
    game.print_board()
    i, j = make_tuple(input("Enter row, col: "))
    game.move_to(i, j)
    game.print_board()
    print("Waiting for AI move ...")
    ai_move, root = mcts(game)
    file.write(jsonpickle.encode(root))
    file.close()
    game.move_to(ai_move[0], ai_move[1])
    finished, winner = game.terminal()
    if finished:
        run = False

print("The winner is " + winner)