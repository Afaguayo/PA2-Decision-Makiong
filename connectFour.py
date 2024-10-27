#Raul Pallares & Angel Aguayo & Natasha Rovelli PA2

from collections import defaultdict
import sys
import random
import math

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

    def simulate_random_game(self):
        current_player = self.current_player
        while True:
            if self.check_win():
                return 1 if current_player == 'Y' else -1
            if self.is_draw():
                return 0
            legal_moves = self.valid_moves()
            if not legal_moves:
                return 0
            move = random.choice(legal_moves)
            self.make_move(move, current_player)
            current_player = 'R' if current_player == 'Y' else 'Y'



def read_board(file_path):
    with open(file_path, 'r') as f:
        algorithm = f.readline().strip()
        current_player = f.readline().strip()
        board = [list(f.readline().strip()) for _ in range(6)]
    return algorithm, current_player, board



def random_move_selection(game):
    valid_moves = game.valid_moves()
    return random.choice(valid_moves) if valid_moves else None



def monte_carlo_search(game, num_simulations, verbosity):
    # Initialize statistics for each column
    win_counts = defaultdict(int)
    visit_counts = defaultdict(int)

    # Perform the simulations
    for _ in range(num_simulations):
        game_clone = game.clone()
        initial_move = None
        path = []

        while True:
            legal_moves = game_clone.valid_moves()
            if not legal_moves:
                break

            # Choose a move at random
            move = random.choice(legal_moves)
            path.append((move, game_clone.current_player))
            if initial_move is None:
                initial_move = move

            # Apply the move
            game_clone.make_move(move, game_clone.current_player)
            if game_clone.check_win() or game_clone.is_draw():
                break

            # Alternate the player
            game_clone.current_player = 'R' if game_clone.current_player == 'Y' else 'Y'

        # Determine the result
        result = 1 if game_clone.current_player == 'Y' else -1 if game_clone.check_win() else 0

        # Update statistics along the path
        for move, player in path:
            visit_counts[move] += 1
            win_counts[move] += result if player == 'Y' else -result

        if verbosity == "Verbose":
            print(f"TERMINAL NODE VALUE: {result}")
            for move in win_counts:
                print(f"Updated values: wi: {win_counts[move]}, ni: {visit_counts[move]}")

    # Calculate the final values for each column
    scores = [win_counts[col] / visit_counts[col] if visit_counts[col] > 0 else "Null" for col in range(7)]
    best_move = max(range(7), key=lambda col: scores[col] if scores[col] != "Null" else float('-inf'))

    # Print final results based on verbosity
    if verbosity in ["Verbose", "Brief"]:
        for col in range(7):
            print(f"Column {col + 1}: {scores[col]}")
    print(f"FINAL Move selected: {best_move + 1}")


def uct(game, numSimulation, current_player, verbosity= "Verbose", c=math.sqrt(2)) :
    win_count = defaultdict(int)
    vist_count = defaultdict(int)

    # Run though simulation
    for i in range(numSimulation):
        clonedGame = game.clone()
        path = []
        initialMove = None

        # Till no moves/terminal
        while True:
            legalMoves = clonedGame.valid_moves()

            if not legalMoves:
                break
            
            # Check if all legal moves tried
            if all(move in vist_count for move in legalMoves):
                totalVists = sum(vist_count[move] for move in legalMoves)
                ucbScores = {}

                #  Cacl UCB score
                for move in legalMoves:
                    winRate = win_count[move] / vist_count[move] if vist_count[move] > 0 else 0
                    ucbScore = winRate + c * math.sqrt(math.log(totalVists)/ (1+ vist_count[move]))
                    ucbScores[move] = ucbScore

                    # Print UCB value
                    if verbosity == "Verbose":
                        print(f"V{move+1}: {ucbScore:.2f}" )
                    # Chose the move with the highest UCB score
                    move = max(ucbScores, key=ucbScores.get)
            else:
                # Choose random unexplored move
                unexploredMoves = [move for move in legalMoves if move not in vist_count]
                move = random.choice(unexploredMoves)
            
            # Track the path taken 
            path.append((move,clonedGame.current_player))
            if initialMove is None:
                initialMove = move
            # Make move
            clonedGame.make_move(move, clonedGame.current_player)
            if clonedGame.check_win() or clonedGame.is_draw():
                break
            # Next players turn
            clonedGame.current_player = 'R' if clonedGame.current_player == 'Y' else 'Y'

        # After simulations 
        result = 1 if clonedGame.current_player == 'Y' else -1 if clonedGame.check_win() else 0

        # Update 
        for move, player in path:
            vist_count[move] +=1
            win_count[move] += result if player == 'Y' else -result
        # Print
        if verbosity == "Verbose":
            print(f"TERMINAL NODE VALUE: {result}")

            for move in win_count:
                print(f"Updated values: wi: {win_count[move]}, ni: {vist_count[move]}")
    # Cal final values for each colum and get best move
    scores = [win_count[col] / vist_count[col] if vist_count[col] > 0 else "Null" for col in range(7)]    
    bestMove = max(range(7), key=lambda col: scores[col] if scores[col] != "Null" else float('-inf'))

    # Print if verbose
    if verbosity in ["Verbose", "Brief"]:
        for col in range(7):
            print(f"Column {col+1}: {scores[col]:.3f}")
    print(f"FINAL Move selected: {bestMove+1}")

    # Return best move 
    return bestMove

def main():
    if len(sys.argv) != 4:
        print("Usage: python connectFour.py <input_file> <verbosity> <num_simulations>")
        return

    input_file = sys.argv[1]
    verbosity = sys.argv[2]
    num_simulations = int(sys.argv[3])  # Not used in UR algorithm

    algorithm, current_player, board = read_board(input_file)
    game = ConnectFour(board, current_player)
    
    if algorithm == 'UR':
        print("UR")
        move = random_move_selection(game)
        print(f"FINAL Move selected: {move + 1}")
    elif algorithm == 'PMCGS':
        print("PMCGS")
        move = monte_carlo_search(game, num_simulations, verbosity)
    elif algorithm == 'UCT':
        print('UCT')
        move = uct(game, num_simulations, current_player, verbosity=verbosity)


if __name__ == "__main__":
    main()
