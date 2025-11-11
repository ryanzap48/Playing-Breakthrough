import random
from tqdm import tqdm

from breakthrough_const import WHITE, BLACK, EMPTY
from games import Game, GameState


class Breakthrough(Game):
    def __init__(self):
        moves = {
            "W": [(-1, 0), (-1, 1), (-1, -1)],  # White moves UP (negative row)
            "B": [(1, 0), (1, -1), (1, 1)],  # Black moves DOWN (positive row)
        }

        board = {0: {}, 1: {WHITE: 0, BLACK: 0}}  # captures

        for c in range(8):
            board[0][(0, c)] = "B"
            board[0][(1, c)] = "B"
            board[0][(6, c)] = "W"
            board[0][(7, c)] = "W"

        self.h, self.v = 8, 8
        self.initial = GameState(to_move=WHITE, utility=0, board=board, moves=moves)

    def actions(self, state):
        turn = state.to_move
        board = state.board[0]
        moves = state.moves
        valid_actions = []

        for (r, c), piece in board.items():
            if (turn == WHITE and piece == "W") or (turn == BLACK and piece == "B"):
                for dr, dc in moves[piece]:
                    new_pos = (r + dr, c + dc)

                    # bounds of board
                    if not (0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8):
                        continue

                    target = board.get(new_pos)

                    # moving forward (piece cannot be there)
                    if dc == 0:
                        if target is None:
                            valid_actions.append(((r, c), new_pos))

                    # can move forward, diagonal if nothing there or opposite piece there
                    else:
                        if target is None or target != piece:
                            valid_actions.append(((r, c), new_pos))

        return valid_actions

    def result(self, state, move):
        (old_pos, new_pos) = move
        board = [dict(state.board[0]), dict(state.board[1])]
        pos_board = board[0]

        # remove old location and add new location
        piece = pos_board[old_pos]
        captured_piece = pos_board.get(new_pos)
        pos_board.pop(old_pos, None)
        pos_board[new_pos] = piece

        if captured_piece == "W":
            board[1][WHITE] += 1
        elif captured_piece == "B":
            board[1][BLACK] += 1

        return GameState(
            to_move=(BLACK if state.to_move == WHITE else WHITE),
            utility=0,
            board=board,
            moves=state.moves,
        )

    def utility(self, state, player):
        """Return the value of this final state to player."""
        board = state.board[0]

        # check if any piece reached opposite side
        for pos, piece in board.items():
            r, _ = pos
            if piece == "W" and r == 0:
                return 1 if player == WHITE else -1
            elif piece == "B" and r == 7:
                return 1 if player == BLACK else -1

        white_pieces = sum(1 for v in board.values() if v == "W")
        black_pieces = sum(1 for v in board.values() if v == "B")
        if white_pieces == 0:
            return 1 if player == BLACK else -1
        elif black_pieces == 0:
            return 1 if player == WHITE else -1

        # game not over
        return 0

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return self.utility(state, state.to_move) != 0 or len(self.actions(state)) == 0

    def display(self, state):
        board = state.board[0]
        print("\n  1 2 3 4 5 6 7 8")
        for r in range(8):
            print(r + 1, end=" ")
            for c in range(8):
                print(board.get((r, c), "."), end=" ")
            print()
        print()

    def get_piece(self, state, r, c):
        board = state.board[0]
        piece = board.get((r, c))
        return {"W": WHITE, "B": BLACK}.get(piece, EMPTY)


def defensive_heuristic_1(state, player):
    board = state.board[0]
    piece = {WHITE: "W", BLACK: "B"}.get(player)
    pieces_remaining = sum(1 for v in board.values() if v == piece)

    return 2 * (pieces_remaining) + random.random()


def offensive_heuristic_1(state, player):
    board = state.board[0]
    opposite_piece = {WHITE: "B", BLACK: "W"}.get(player)
    opposite_pieces_remaining = sum(1 for v in board.values() if v == opposite_piece)

    return 2 * (32 - opposite_pieces_remaining) + random.random()


def defensive_heuristic_2(state, player):
    board = state.board[0]
    piece = {WHITE: "W", BLACK: "B"}.get(player)
    opposite_piece = {WHITE: "B", BLACK: "W"}.get(player)
    direction = -1 if piece == "W" else 1

    pieces_remaining = 0
    protected = 0
    back_line_defense = 0
    enemy_near_goal = 0
    enemy_threats = 0

    for (r, c), v in board.items():
        if v == piece:
            pieces_remaining += 1

            for dc in [-1, 1]:

                # piece diagonal to same piece in case of capture
                if board.get((r - direction, c + dc)) == piece:
                    protected += 1

            # more pieces in back rows for defence
            if (piece == "W" and r >= 6) or (piece == "B" and r <= 1):
                back_line_defense += 1

        elif v == opposite_piece:
            # oppsite pieces are close to wining
            if (piece == "W" and r >= 5) or (piece == "B" and r <= 3):
                enemy_near_goal += 1

            # opposite pieces are close to pieces
            for dc in [-1, 0, 1]:
                if board.get((r + direction, c + dc)) == piece:
                    enemy_threats += 1

    return (
        4 * pieces_remaining + 5 * protected - 7 * enemy_near_goal - 5 * enemy_threats + 10 * back_line_defense + random.random() * 0.01
    )


def offensive_heuristic_2(state, player):
    board = state.board[0]
    piece = {WHITE: "W", BLACK: "B"}.get(player)
    opposite_piece = {WHITE: "B", BLACK: "W"}.get(player)
    direction = -1 if piece == "W" else 1

    advancement, captures, enemy_count = 0, 0, 0

    for (r, c), v in board.items():
        if v == piece:
            # rewarded for moving forward
            if piece == "W":
                advancement += 7 - r
            else:
                advancement += r

            # rewards for capturing pieces
            for cy in [-1, 1]:
                if board.get((r + direction, c + cy)) == opposite_piece:
                    captures += 1

        elif v == opposite_piece:
            enemy_count += 1

    return (
        2 * (32 - enemy_count) + 2 * advancement + 4 * captures + random.random() * 0.01
    )


def play_game(white_agent, black_agent, max_moves=400, display=False, progress=False):
    """
    Run a round of game with specified agents. Returns the statistic of the gameplay.

    :param white_agent: An agent that plays white.
    :param black_agent: An agent that plays black.
    :param max_moves: The maximum number of moves to play.
    :param display: Whether to display the game state during play.
    :param progress: Whether to show a progress bar.
    :return: The statistic of the game play.
    """
    game = Breakthrough()

    state = game.initial
    move_count = 0
    if progress:
        pbar = tqdm(total=max_moves, desc="Game in progress", ncols=100)
    while True:
        move = (
            white_agent.select_move(game, state)
            if state.to_move == WHITE
            else black_agent.select_move(game, state)
        )
        state = game.result(state, move)
        if display:
            game.display(state)
        move_count += 1
        if progress:
            pbar.update()
        if game.terminal_test(state) or move_count >= max_moves:
            captures = state.board[1]
            if move_count <= max_moves:
                winner = WHITE if state.to_move == BLACK else BLACK
            else:
                winner = None
            break
    if progress:
        pbar.close()
    white_nodes = sum(white_agent.nodes_per_move)
    black_nodes = sum(black_agent.nodes_per_move)

    white_time_per_move = sum(white_agent.time_per_move) / len(
        white_agent.time_per_move
    )
    black_time_per_move = sum(black_agent.time_per_move) / len(
        black_agent.time_per_move
    )
    white_nodes_per_move = white_nodes / len(white_agent.nodes_per_move)
    black_nodes_per_move = black_nodes / len(black_agent.nodes_per_move)

    white_captures = captures[WHITE]
    black_captures = captures[BLACK]
    if display:
        game.display(state)
    return {
        "winner": "white" if winner == WHITE else "black" if winner == BLACK else None,
        "white_name": white_agent.name,
        "black_name": black_agent.name,
        "total_moves": move_count,
        "white_nodes": white_nodes,
        "black_nodes": black_nodes,
        "white_nodes_per_move": white_nodes_per_move,
        "black_nodes_per_move": black_nodes_per_move,
        "white_time_per_move": white_time_per_move,
        "black_time_per_move": black_time_per_move,
        "white_captures": white_captures,
        "black_captures": black_captures,
    }


if __name__ == "__main__":
    from breakthrough_agent import MinimaxAgent, AlphaBetaAgent

    game = Breakthrough()
    white_agent = AlphaBetaAgent(
        "AlphaBeta Off1", depth=4, eval_fn=defensive_heuristic_2
    )
    black_agent = AlphaBetaAgent(
        "AlphaBeta Def1", depth=4, eval_fn=defensive_heuristic_1
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)
