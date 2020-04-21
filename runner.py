import jsonpickle
from ast import literal_eval as make_tuple

from game import Game, x, o
from ai import MCTS


game = Game(7, 4, x)

run = True

while run:
    game.print_board()
    i, j = make_tuple(input("Enter row, col: "))
    game.move_to(i, j)
    game.print_board()

    finished, winner = game.terminal()
    if finished:
        run = False

    print("Waiting for AI move ... ")
    agent = MCTS.load(game_state=game, playing_as=o)
    ai_move = agent.mcts()
    game.move_to(ai_move[0], ai_move[1])

    finished, winner = game.terminal()
    if finished:
        run = False

print("The winner is " + winner)
