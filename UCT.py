import math
import random
class Node:
    def __init__(self, move =None, parent=None):
        self.parent = parent
        self.move = move
        self.wi = 0
        self.ni = 0
        self.children = {}

    def addNode(self,move):
        if move not in self.children:
            self.children[move] = Node(move=move, parent=self)
        return self.children[move]
    
    def update_wi_ni(self, result,verbose= "Verbose"):
        self.wi += result
        self.ni += 1

        if verbose== "Verbose":

            print("Updated values: ")
            print("wi: ", self.wi)
            print("ni: ", self.ni)
    
    def ucbFormula(self, c=math.sqrt(2), verbose="Verbose"):
        bestUCB = float('-inf')
        bestChild = None

        # Debugging to ensure `c` is a float
        if not isinstance(c, float):
            print("Warning: 'c' is expected to be a float, but got:", type(c))
            c = float(c)  # Explicitly cast `c` to float if it's not

        for move, child in self.children.items():
            if child.ni == 0:
                value = float('inf')
            else:
                # Additional debug output to confirm types and values
                
                #debugging print
                #print(f"Calculating UCB for move {move + 1}: child.wi={child.wi} ({type(child.wi)}), "   
                #    f"child.ni={child.ni} ({type(child.ni)}), self.ni={self.ni} ({type(self.ni)}), c={c} ({type(c)})")
                
                value = (child.wi / child.ni) + c * math.sqrt(math.log(self.ni) / child.ni)

            if verbose == "Verbose":
                print("UCB value for move", move + 1, ":", value)

            if value > bestUCB:
                bestUCB = value
                bestChild = child

        return bestChild


    

class UCTree:
    def __init__(self):
        self.root = Node()


    def rollout(self, game, numSimulations, player, verbose="Verbose"):
        for i in range(numSimulations):
            clonedGame = game.clone()  # Clone the current game state
            clonedGame.current_player = player  # Set the current player
            node = self.root  # Start from the root node

            while not clonedGame.check_win() and not clonedGame.is_draw():
                legalMoves = clonedGame.valid_moves()  # Get the list of valid moves

                # If all legal moves have been explored, use UCB to select the best child node
                if node.children and len(node.children) == len(legalMoves):
                    node = node.ucbFormula(c=math.sqrt(2), verbose=verbose)  # Corrected call
                    move = node.move
                else:
                    # Explore an unexplored move
                    unexploredMoves = [move for move in legalMoves if move not in node.children]
                    move = random.choice(unexploredMoves)
                    node = node.addNode(move)  # Add the new node for the unexplored move

                    if verbose == "Verbose":
                        print("NODE ADDED")

                # Make the move in the cloned game
                clonedGame.make_move(move, clonedGame.current_player)
                # Switch players
                clonedGame.current_player = 'Y' if clonedGame.current_player == 'R' else 'R'

                if verbose == "Verbose":
                    print("Move selected: ", move + 1)

            # Determine the result of the game simulation
            if clonedGame.is_draw():
                result = 0
            else:
                result = 1 if clonedGame.current_player == 'Y' else -1

            if verbose == "Verbose":
                print("TERMINAL NODE VALUE: ", result)

            # Update the nodes with the result
            self.updateNodes(node, result, verbose)


    def updateNodes(self, node, result, verbose  = "Verbose"):
         while node is not None:
             node.update_wi_ni(result, verbose)
             node = node.parent

    def finalMoveSelection(self, verbose="Verbose"):
        scores = {}

        for move, child in self.root.children.items():
            if child.ni > 0:
                scores[move] = child.wi / child.ni
            else:
                scores[move] = "Null"

        bestMove = None
        bestScore = -float('inf')  # Initialize to negative infinity for max comparison

        for move, score in scores.items():
            if score != "Null" and score > bestScore:
                bestMove = move
                bestScore = score

        if verbose in ["Brief", "Verbose"]:
            for move, score in scores.items():
                print(f"Column {move + 1}: {score}")
        return bestMove

    
