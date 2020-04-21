from abc import ABC

from game import Game, x, o
import copy
import random
import math


class AbstractNode(ABC):
    def __init__(self):
        self.parent = None
        self.action = None
        self.children = []
        self.weight = 0
        self.simulations = 0


class RootNode(AbstractNode):
    """A root node for the MCTS algorithm"""

    def __init__(self, game_state: Game):
        super().__init__()
        self.game_state = copy.deepcopy(game_state)
        self.children = []


class Node(AbstractNode):
    """A child node in MCTS tree"""

    def __init__(self, parent, action):
        super().__init__()
        self.action = action
        self.parent = parent
        self.weight = 0
        self.simulations = 0
        self.children = []

    def get_avg(self):
        return self.weight / self.simulations


class MCTS:
    """Wrapper for MCTS algorithm at a specific game state"""

    def __init__(self, game_state: Game, playing_as, max_iterations=10000):
        self.root = RootNode(game_state)
        self.max_iterations = max_iterations
        self.playing_as = playing_as

    def get_game_state(self, node: Node) -> Game:
        """Generate the game state at the given node"""

        path = []
        current = node
        while current is not None and current.action is not None:
            path.append(current.action)
            current = current.parent
        base_game = copy.deepcopy(self.root.game_state)
        game_state = Game.chain_result(base_game, path[::-1])

        return game_state

    def traverse(self) -> Node:
        """Return the node to start a play out from"""
        node = self.root

        while len(node.children):
            node = self.ucb_best(node.children)

        self.expand(node)

        if len(node.children):
            return node.children[0]

        return node

    def play_out(self, game: Game):
        """Play out the game with a random selection policy"""
        terminated, the_winner = game.terminal()

        if terminated:
            if the_winner is None:
                return 0
            elif the_winner == self.playing_as:
                return 1
            else:
                return -1

        return self.play_out(Game.result(game, random.choice(game.actions())))

    def update_and_propagate(self, node, result):
        """Update the current node stats with the given result, and propagate"""
        node.weight += result
        node.simulations += 1

        if node.parent:
            self.update_and_propagate(node.parent, result)

    def expand(self, node):
        """Expand the given node by all possible actions"""
        game_state = self.get_game_state(node)

        for action in game_state.actions():
            n = Node(node, action)
            node.children.append(n)

    @staticmethod
    def ucb(node):
        """Calculate the UCB1 value for the given node"""
        return node.get_avg() + math.sqrt(2) * math.sqrt(math.log(node.parent.simulations) / node.simulations)

    def ucb_best(self, nodes) -> Node:
        """Return the node with highest UCB1 value"""
        for node in nodes:
            if node.simulations == 0:
                return node

        return max(nodes, key=lambda n: self.ucb(n))

    def mcts(self):
        """Apply the MCTS algorithm from the root and return the best action"""

        for i in range(self.max_iterations):
            nxt_node = self.traverse()
            game_state = self.get_game_state(nxt_node)
            node_value = self.play_out(game_state)
            self.update_and_propagate(nxt_node, node_value)

            if i % 100 == 0:
                print(str(i) + "/" + str(self.max_iterations), end='\r')

        best_node = max(self.root.children, key=lambda n: n.get_avg())

        return best_node.action
