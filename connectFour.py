#Raul Pallares & Angel Aguayo PA2

import sys
import random

class ConnectFour:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player

    def valid_moves(self):
        return [col for col in range(7) if self.board[0][col] == 'O']

    def make_move(self, col, player):
        for row in range(5, -1, -1):
            if self.board[row][col] == 'O':
                self.board[row][col] = player
                break

    def check_win(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] != 'O' and self.check_direction(row, col):
                    return True
        return False

    def check_direction(self, row, col):
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            if self.check_line(row, col, dr, dc, player):
                return True
        return False

    def check_line(self, row, col, dr, dc, player):
        count = 0
        for i in range(4):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                count += 1
            else:
                break
        return count == 4

    def is_draw(self):
        return all(self.board[0][col] != 'O' for col in range(7))

    def clone(self):
        return ConnectFour([row[:] for row in self.board], self.current_player)

def read_board(file_path):
    with open(file_path, 'r') as f:
        algorithm = f.readline().strip()
        current_player = f.readline().strip()
        board = [list(f.readline().strip()) for _ in range(6)]
    return algorithm, current_player, board

def random_move_selection(game):
    valid_moves = game.valid_moves()
    return random.choice(valid_moves)

def main():
    if len(sys.argv) != 4:
        print("Usage: python connectFour.py <input_file> <verbosity> <num_simulations>")
        return

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    num_simulations = int(sys.argv[3])  # Not used in UR algorithm

    algorithm, current_player, board = read_board(input_file)
    game = ConnectFour(board, current_player)

    print(f"Starting Player: {current_player}")
    print("Initial Board:")
    for row in board:
        print(''.join(row))

    while True:
        if algorithm == 'Random' or algorithm == 'UR':
            move = random_move_selection(game)
        else:
            print("Unknown algorithm specified.")
            return

        if verbosity == 'Verbose':
            print(f"Player {game.current_player} chose move: {move + 1}")

        game.make_move(move, game.current_player)

        if verbosity != 'None':
            for row in game.board:
                print(''.join(row))
            print()

        if game.check_win():
            print(f"Player {game.current_player} wins!")
            break
        elif game.is_draw():
            print("The game is a draw!")
            break

        game.current_player = 'Y' if game.current_player == 'R' else 'R'

if __name__ == "__main__":
    main()
