import sys

def load_puzzle(filename):
    if not filename.endswith(".txt"):
        sys.exit("File Error: Input file must be a text file")

    puzzle = []
    with open(filename) as f:
        contents = f.read().splitlines()
        for i in range(9):
            if len(contents[i]) != 9 or not contents[i].isnumeric(): sys.exit("File Error: Input file is not in correct format")
            puzzle.append([])
            for j in range(9):
                puzzle[i].append(int(contents[i][j]))

    return puzzle

def printSolution(sol):
	for i in range(9):
		if i % 3 == 0: print("+-----+-----+-----+")
		for j in range(9):
			if j % 3 == 0: print("|" + str(sol[i][j]), end="")
			else: print(" " + str(sol[i][j]), end="")
		print("|\r")
	print("+-----+-----+-----+")
	
def printMoves(moves, guess=False, depth=0):
	indent = " " * depth * 2
	if guess:
		start = 1
	else:
		start = 0
	for i, move in enumerate(moves[start:]):
		if type(move) == list:
			print(indent + f"Guess: {move[0]}")
			printMoves(move, guess=True, depth=depth+1)
		else:
			if i == len(moves[start:]) - 1: print(indent + f"{move}") 
			else: print(indent + f"Implied: {move}")
			
			
      
def save_solution(filename, solvedPuzzle):
	with open(filename, "w") as f:
		for line in solvedPuzzle:
			for number in line:
				f.write(str(number))
			f.write("\n")