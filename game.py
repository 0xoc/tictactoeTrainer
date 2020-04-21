empty = ""
o = "O"
x = "x"


class Game:
    def __init__(self, size: int, win_count: int, playing_as):
        self.playing_as = playing_as  # playing as X or O
        self.win_count = win_count  # number of X's or O's in a line to win
        self.size = size  # size of the board
        self.board = [[empty for j in range(size)] for i in range(size)]  # initialize the board

    def boxes(self, box_size: int) -> list[list]:
        """A list of all possible distinct box_size x box_size boxes in the bord"""
        assert (box_size >= self.size)

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
