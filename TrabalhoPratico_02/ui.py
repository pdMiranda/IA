import pygame
from ai import AI

class UI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.Font(None, 200)
        self.small_font = pygame.font.Font(None, 36)
        self.ai = None
        self.show_menu = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.show_menu:
            x, y = event.pos
            if 100 <= x <= 500 and 100 <= y <= 150:
                self.ai = AI("bfs")
                self.game.ai = self.ai
                self.show_menu = False
            elif 100 <= x <= 500 and 175 <= y <= 225:
                self.ai = AI("dfs")
                self.game.ai = self.ai
                self.show_menu = False
            elif 100 <= x <= 500 and 250 <= y <= 300:
                self.ai = AI("minimax")
                self.game.ai = self.ai
                self.show_menu = False
            elif 100 <= x <= 500 and 325 <= y <= 375:
                self.ai = AI("a_star_h1")
                self.game.ai = self.ai
                self.show_menu = False
            elif 100 <= x <= 500 and 400 <= y <= 450:
                self.ai = AI("a_star_h2")
                self.game.ai = self.ai
                self.show_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.show_menu:
            x, y = event.pos
            if self.game.game_over:
                return
            row, col = y // 200, x // 200
            if self.game.make_move(row * 3 + col):
                if not self.game.game_over:
                    move = self.game.ai.get_move(self.game.board)
                    self.game.make_move(move)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.reset()
            elif event.key == pygame.K_r:
                self.game.reset()
                self.show_menu = True

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        if self.show_menu:
            self.draw_menu()
        else:
            self.draw_board()
            self.highlight_winning_combo()

    def draw_menu(self):
        bfs_button = pygame.Rect(100, 100, 400, 50)
        dfs_button = pygame.Rect(100, 175, 400, 50)
        minimax_button = pygame.Rect(100, 250, 400, 50)
        astar1_button = pygame.Rect(100, 325, 400, 50)
        astar2_button = pygame.Rect(100, 400, 400, 50)

        pygame.draw.rect(self.screen, (100, 100, 200), bfs_button)
        pygame.draw.rect(self.screen, (100, 200, 100), dfs_button)
        pygame.draw.rect(self.screen, (200, 100, 100), minimax_button)
        pygame.draw.rect(self.screen, (200, 200, 100), astar1_button)
        pygame.draw.rect(self.screen, (100, 200, 200), astar2_button)

        bfs_text = self.small_font.render("Busca em Largura", True, (255, 255, 255))
        dfs_text = self.small_font.render("Busca em Profundidade", True, (255, 255, 255))
        minimax_text = self.small_font.render("MINIMAX", True, (255, 255, 255))
        astar1_text = self.small_font.render("A* Heurística 1", True, (255, 255, 255))
        astar2_text = self.small_font.render("A* Heurística 2", True, (255, 255, 255))

        self.screen.blit(bfs_text, (bfs_button.centerx - bfs_text.get_width() // 2, bfs_button.centery - bfs_text.get_height() // 2))
        self.screen.blit(dfs_text, (dfs_button.centerx - dfs_text.get_width() // 2, dfs_button.centery - dfs_text.get_height() // 2))
        self.screen.blit(minimax_text, (minimax_button.centerx - minimax_text.get_width() // 2, minimax_button.centery - minimax_text.get_height() // 2))
        self.screen.blit(astar1_text, (astar1_button.centerx - astar1_text.get_width() // 2, astar1_button.centery - astar1_text.get_height() // 2))
        self.screen.blit(astar2_text, (astar2_button.centerx - astar2_text.get_width() // 2, astar2_button.centery - astar2_text.get_height() // 2))

    def draw_board(self):
        for row in range(3):
            for col in range(3):
                rect = pygame.Rect(col * 200, row * 200, 200, 200)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
                if self.game.board[row * 3 + col] == 'X':
                    self.screen.blit(self.font.render('X', True, (0, 0, 0)), (col * 200 + 50, row * 200 + 25))
                elif self.game.board[row * 3 + col] == 'O':
                    self.screen.blit(self.font.render('O', True, (0, 0, 0)), (col * 200 + 50, row * 200 + 25))

    def highlight_winning_combo(self):
        if self.game.winner and self.game.winner != 'Draw':
            for idx in self.game.winning_combo:
                row, col = divmod(idx, 3)
                rect = pygame.Rect(col * 200, row * 200, 200, 200)
                color = (0, 255, 0) if self.game.winner == 'X' else (255, 0, 0)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
                self.screen.blit(self.font.render(self.game.winner, True, (0, 0, 0)), (col * 200 + 50, row * 200 + 25))
        elif self.game.winner == 'Draw':
            self.screen.fill((255, 255, 0))
            self.draw_board()
