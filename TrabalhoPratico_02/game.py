class Game:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None
        self.winning_combo = None
        self.ai = None
        self.game_over = False

    def reset(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None
        self.winning_combo = None
        self.game_over = False

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            if self.check_winner():
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winner = self.board[combo[0]]
                self.winning_combo = combo
                return True
        if ' ' not in self.board:
            self.winner = 'Draw'
            return True
        return False
    
    def game_over(self):
        return self.game_over
