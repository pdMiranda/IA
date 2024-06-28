import time
import random
from ai import AI
from game import Game

def run_tests():
    game = Game()
    results = {}

    algorithms = ["bfs", "dfs", "minimax", "a_star_h1", "a_star_h2"]
    for algo in algorithms:
        print(f"Testing algorithm: {algo}")
        ai = AI(algo)
        total_moves = 0
        total_tests = 0

        start_time = time.time()

        while not game.game_over:  # Correção: corrigido o loop while
            current_player = game.current_player
            if current_player == 'X':  # Jogador humano (X)
                available_moves = [i for i in range(9) if game.board[i] == ' ']  # Movimentos disponíveis
                move = random.choice(available_moves)  # Escolhe um movimento aleatório
                game.make_move(move)
                total_moves += 1
            elif current_player == 'O':  # Jogador IA (O)
                move_info = ai.get_move(game.board)  # Obter movimento
                if isinstance(move_info, tuple):
                    move, num_tests = move_info
                else:
                    move = move_info
                    num_tests = 0  # Define um valor padrão para num_tests se get_move não retornar um tuple
                game.make_move(move)
                total_moves += 1
                total_tests += num_tests  # Adicionar número de testes realizados

        end_time = time.time()
        total_time = end_time - start_time

        winner = determine_winner(game)  # Determina o vencedor do jogo

        results[algo] = {
            "time": total_time,
            "moves_count": total_moves,
            "winner": winner
        }

        game.reset()

    generate_report(results)

def determine_winner(game):
    winner = game.check_winner()
    if winner == 'X':
        return 'Player'
    elif winner == 'O':
        return 'IA'
    else:
        return 'Draw'

def generate_report(results):
    print("\n=== Relatório de Testes ===\n")

    for algo, data in results.items():
        print(f"Algoritmo: {algo}")
        print(f"Tempo total: {data['time']:.4f} segundos")
        print(f"Número total de movimentos: {data['moves_count']}")
        print(f"Vencedor: {data['winner']}")
        print("--------------------")

    # Comparação de desempenho (exemplo: tempo médio)
    average_times = {algo: data['time'] for algo, data in results.items()}
    best_algorithm = min(average_times, key=average_times.get)
    print(f"\nMelhor algoritmo: {best_algorithm} (menor tempo médio - {average_times[min(average_times, key=average_times.get)]} milissegundos)")

if __name__ == "__main__":
    run_tests()
