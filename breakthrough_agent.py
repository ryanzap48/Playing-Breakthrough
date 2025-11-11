import time


def minimax_cutoff_search(game, state, d=3, cutoff_test=None, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states or reaching a cutoff
    point. Return the action and number of nodes expanded."""

    player = state.to_move
    nodes = 0

    def cutoff(state, depth):
        return depth >= d or game.terminal_test(state)

    def max_value(state, depth):
        nonlocal nodes
        nodes += 1
        if cutoff(state, depth):
            return eval_fn(state, player)
        maxEval = -float("inf")

        for action in game.actions(state):
            maxEval = max(maxEval, min_value(game.result(state, action), depth + 1))
        return maxEval

    def min_value(state, depth):
        nonlocal nodes
        nodes += 1
        if cutoff(state, depth):
            return eval_fn(state, player)
        minEval = float("inf")

        for action in game.actions(state):
            minEval = min(minEval, max_value(game.result(state, action), depth + 1))
        return minEval

    best_score = -float("inf")
    best_action = None

    for action in game.actions(state):
        eval = min_value(game.result(state, action), 1)
        if eval > best_score:
            best_score = eval
            best_action = action

    return best_action, nodes


def alpha_beta_cutoff_search(game, state, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    Return the action and number of nodes expanded."""

    player = state.to_move
    nodes = 0

    def cutoff(state, depth):
        return depth >= d or game.terminal_test(state)

    def max_value(state, depth, alpha, beta):
        nonlocal nodes
        nodes += 1
        if cutoff(state, depth):
            return eval_fn(state, player)

        maxEval = -float("inf")

        for action in game.actions(state):
            maxEval = max(
                maxEval, min_value(game.result(state, action), depth + 1, alpha, beta)
            )
            if maxEval >= beta:
                return maxEval
            alpha = max(alpha, maxEval)
        return maxEval

    def min_value(state, depth, alpha, beta):
        nonlocal nodes
        nodes += 1
        if cutoff(state, depth):
            return eval_fn(state, player)
        minEval = float("inf")

        for action in game.actions(state):
            minEval = min(
                minEval, max_value(game.result(state, action), depth + 1, alpha, beta)
            )
            if minEval <= alpha:
                return minEval
            beta = min(beta, minEval)
        return minEval

    best_score = -float("inf")
    best_action = None

    alpha, beta = -float("inf"), float("inf")

    for action in game.actions(state):
        eval = min_value(game.result(state, action), 1, alpha, beta)
        if eval > best_score:
            best_score = eval
            best_action = action
        alpha = max(alpha, eval)

    return best_action, nodes


class BaseAgent:
    def __init__(self, name, depth, cutoff_test, eval_fn):
        self.name = name
        self.depth = depth
        self.cutoff_test = cutoff_test
        self.eval_fn = eval_fn
        self.time_per_move = []
        self.nodes_per_move = []

    def select_move(self, game, state):
        raise NotImplementedError

    def reset(self):
        self.time_per_move = []
        self.nodes_per_move = []


class MinimaxAgent(BaseAgent):
    def __init__(self, name, depth=3, cutoff_test=None, eval_fn=None):
        super().__init__(name, depth, cutoff_test, eval_fn)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = minimax_cutoff_search(
            game, state, self.depth, self.cutoff_test, self.eval_fn
        )
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move


class AlphaBetaAgent(BaseAgent):
    def __init__(self, name, depth=6, cutoff_test=None, eval_fn=None):
        super().__init__(name, depth, cutoff_test, eval_fn)

    def select_move(self, game, state):
        t0 = time.perf_counter()
        move, nodes = alpha_beta_cutoff_search(
            game, state, self.depth, self.cutoff_test, self.eval_fn
        )
        dt = time.perf_counter() - t0
        self.time_per_move.append(dt)
        self.nodes_per_move.append(nodes)
        return move
