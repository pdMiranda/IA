import random

class AI:
    def __init__(self, ai_type):
        self.ai_type = ai_type

    def get_move(self, board):
        if self.ai_type == "bfs":
            return self.bfs(board)
        elif self.ai_type == "dfs":
            return self.dfs(board)
        elif self.ai_type == "minimax":
            return self.minimax(board)
        elif self.ai_type == "a_star_h1":
            return self.a_star(board, self.heuristic1)
        elif self.ai_type == "a_star_h2":
            return self.a_star(board, self.heuristic2)

    def is_winner(self, board, player):
        combinacoes_vencedoras = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in combinacoes_vencedoras:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return True
        return False

    def bfs(self, board):
        from collections import deque

        fila = deque([(board, 'O')])
        while fila:
            tabuleiro_atual, jogador = fila.popleft()
            for i in range(9):
                if tabuleiro_atual[i] == ' ':
                    novo_tabuleiro = tabuleiro_atual[:]
                    novo_tabuleiro[i] = jogador
                    print(f"BFS testando jogada {i} para jogador {jogador}: {novo_tabuleiro}")
                    if self.is_winner(novo_tabuleiro, 'O'):
                        print(f"BFS encontrou jogada vencedora {i}")
                        return i
                    if self.is_winner(novo_tabuleiro, 'X'):
                        print(f"BFS bloqueando jogada do jogador {i}")
                        return i
                    fila.append((novo_tabuleiro, 'X' if jogador == 'O' else 'O'))
        
        jogada_fallback = random.choice([i for i, x in enumerate(board) if x == ' '])
        print(f"BFS jogada de fallback {jogada_fallback}")
        return jogada_fallback

    def dfs(self, board):
        pilha = [(board, 'O')]
        while pilha:
            tabuleiro_atual, jogador = pilha.pop()
            for i in range(9):
                if tabuleiro_atual[i] == ' ':
                    novo_tabuleiro = tabuleiro_atual[:]
                    novo_tabuleiro[i] = jogador
                    print(f"DFS testando jogada {i} para jogador {jogador}: {novo_tabuleiro}")
                    if self.is_winner(novo_tabuleiro, 'O'):
                        print(f"DFS encontrou jogada vencedora {i}")
                        return i
                    if self.is_winner(novo_tabuleiro, 'X'):
                        print(f"DFS bloqueando jogada do jogador {i}")
                        return i
                    pilha.append((novo_tabuleiro, 'X' if jogador == 'O' else 'O'))
        
        jogada_fallback = random.choice([i for i, x in enumerate(board) if x == ' '])
        print(f"DFS jogada de fallback {jogada_fallback}")
        return jogada_fallback

    def minimax(self, board):
        def minimax_recursivo(board, profundidade, maximizando):
            if self.is_winner(board, 'O'):
                return 1
            if self.is_winner(board, 'X'):
                return -1
            if ' ' not in board:
                return 0

            if maximizando:
                melhor_pontuacao = -float('inf')
                for i in range(9):
                    if board[i] == ' ':
                        board[i] = 'O'
                        pontuacao = minimax_recursivo(board, profundidade + 1, False)
                        board[i] = ' '
                        print(f"Minimax (max) testando jogada {i} com score {pontuacao}")
                        melhor_pontuacao = max(pontuacao, melhor_pontuacao)
                return melhor_pontuacao
            else:
                melhor_pontuacao = float('inf')
                for i in range(9):
                    if board[i] == ' ':
                        board[i] = 'X'
                        pontuacao = minimax_recursivo(board, profundidade + 1, True)
                        board[i] = ' '
                        print(f"Minimax (min) testando jogada {i} com score {pontuacao}")
                        melhor_pontuacao = min(pontuacao, melhor_pontuacao)
                return melhor_pontuacao

        melhor_pontuacao = -float('inf')
        melhor_jogada = None
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                pontuacao = minimax_recursivo(board, 0, False)
                board[i] = ' '
                print(f"Minimax testando jogada {i} com score {pontuacao}")
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_jogada = i

        print(f"Minimax escolheu a jogada {melhor_jogada} com score {melhor_pontuacao}")
        return melhor_jogada

    def a_star(self, board, heuristic):
        from heapq import heappop, heappush

        def vizinhos(tabuleiro_atual, jogador):
            for i in range(9):
                if tabuleiro_atual[i] == ' ':
                    novo_tabuleiro = tabuleiro_atual[:]
                    novo_tabuleiro[i] = jogador
                    yield novo_tabuleiro, i

        def objetivo(tabuleiro_atual, jogador):
            return self.is_winner(tabuleiro_atual, jogador) or self.is_winner(tabuleiro_atual, 'X' if jogador == 'O' else 'O')

        lista_aberta = [(0, board, 'O')]
        veio_de = {str(board): None}
        g_score = {str(board): 0}
        f_score = {str(board): heuristic(board, 'O')}

        while lista_aberta:
            _, atual, jogador = heappop(lista_aberta)

            if objetivo(atual, jogador):
                # Retrocede para encontrar o caminho que levou ao objetivo
                ultima_jogada = None
                while veio_de[str(atual)] is not None:
                    atual, jogada = veio_de[str(atual)]
                    ultima_jogada = jogada
                return ultima_jogada

            for proximo_tabuleiro, jogada in vizinhos(atual, jogador):
                g_score_tentativo = g_score[str(atual)] + 1
                if str(proximo_tabuleiro) not in g_score or g_score_tentativo < g_score[str(proximo_tabuleiro)]:
                    veio_de[str(proximo_tabuleiro)] = (atual, jogada)
                    g_score[str(proximo_tabuleiro)] = g_score_tentativo
                    f_score[str(proximo_tabuleiro)] = g_score[str(proximo_tabuleiro)] + heuristic(proximo_tabuleiro, 'X' if jogador == 'O' else 'O')
                    heappush(lista_aberta, (f_score[str(proximo_tabuleiro)], proximo_tabuleiro, 'X' if jogador == 'O' else 'O'))

        jogada_fallback = random.choice([i for i, x in enumerate(board) if x == ' '])
        return jogada_fallback

    def heuristic1(self, board, player):
        oponente = 'O' if player == 'X' else 'X'
        linhas_jogador = 0
        linhas_oponente = 0

        combinacoes_vencedoras = [
            [board[0], board[1], board[2]], [board[3], board[4], board[5]], [board[6], board[7], board[8]],  # Linhas
            [board[0], board[3], board[6]], [board[1], board[4], board[7]], [board[2], board[5], board[8]],  # Colunas
            [board[0], board[4], board[8]], [board[2], board[4], board[6]]   # Diagonais
        ]

        for combo in combinacoes_vencedoras:
            if combo.count(player) == 3:  # Jogador atual ganha
                linhas_jogador += 1
            elif combo.count(oponente) == 3:  # Oponente ganha (bloqueio)
                linhas_oponente += 1

        return linhas_jogador - linhas_oponente

    def heuristic2(self, board, player):
        oponente = 'O' if player == 'X' else 'X'

        # Calcula a distância mínima para o jogador atual (X ou O) ganhar
        def min_distancia_para_vencer(board, player):
            min_movimentos = float('inf')
            combinacoes_vencedoras = [
                [board[0], board[1], board[2]], [board[3], board[4], board[5]], [board[6], board[7], board[8]],  # Linhas
                [board[0], board[3], board[6]], [board[1], board[4], board[7]], [board[2], board[5], board[8]],  # Colunas
                [board[0], board[4], board[8]], [board[2], board[4], board[6]]   # Diagonais
            ]

            for combo in combinacoes_vencedoras:
                if combo.count(player) == 2 and combo.count(' ') == 1:  # Uma jogada para vitória
                    min_movimentos = min(min_movimentos, combo.count(' '))
            return min_movimentos

        # Calcula a distância mínima para X e O ganharem
        distancia_para_vencer_jogador = min_distancia_para_vencer(board, player)
        distancia_para_vencer_oponente = min_distancia_para_vencer(board, oponente)

        return min(distancia_para_vencer_jogador, distancia_para_vencer_oponente)
