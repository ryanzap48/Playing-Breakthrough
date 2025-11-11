from breakthrough import offensive_heuristic_1, defensive_heuristic_1
from breakthrough import offensive_heuristic_2, defensive_heuristic_2
from breakthrough import play_game
from breakthrough_agent import MinimaxAgent, AlphaBetaAgent


def main():
    white_agent = MinimaxAgent("Minimax Off1", depth=4, eval_fn=offensive_heuristic_1)
    black_agent = AlphaBetaAgent(
        "AlphaBeta Off1", depth=5, eval_fn=offensive_heuristic_1
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)

    white_agent = AlphaBetaAgent(
        "AlphaBeta Off2", depth=5, eval_fn=offensive_heuristic_2
    )
    black_agent = AlphaBetaAgent(
        "AlphaBeta Def1", depth=5, eval_fn=defensive_heuristic_1
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)

    white_agent = AlphaBetaAgent(
        "AlphaBeta Def2", depth=5, eval_fn=defensive_heuristic_2
    )
    black_agent = AlphaBetaAgent(
        "AlphaBeta Off1", depth=5, eval_fn=offensive_heuristic_1
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)

    white_agent = AlphaBetaAgent(
        "AlphaBeta Off2", depth=5, eval_fn=offensive_heuristic_2
    )
    black_agent = AlphaBetaAgent(
        "AlphaBeta Off1", depth=5, eval_fn=offensive_heuristic_1
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)

    white_agent = AlphaBetaAgent(
        "AlphaBeta Def2", depth=5, eval_fn=defensive_heuristic_2
    )
    black_agent = AlphaBetaAgent(
        "AlphaBeta Def1", depth=5, eval_fn=defensive_heuristic_1
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)

    white_agent = AlphaBetaAgent(
        "AlphaBeta Off2", depth=5, eval_fn=offensive_heuristic_2
    )
    black_agent = AlphaBetaAgent(
        "AlphaBeta Def2", depth=5, eval_fn=defensive_heuristic_2
    )
    results = play_game(
        white_agent, black_agent, max_moves=400, display=True, progress=True
    )
    print(results)


if __name__ == "__main__":
    main()
