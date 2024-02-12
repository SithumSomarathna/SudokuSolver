import sys
import solver
import IO
import visualiser
import config


def main():

	puzzle = []
	if config.INPUT == "File":
		filename = input("Enter puzzle filename: ")
		puzzle = IO.load_puzzle(filename)
	elif config.INPUT == "Screen":
		puzzle = [[0 for _ in range(9)] for _ in range(9)]
		board = visualiser.Board()
		board.inputMoves(puzzle)

	solvedPuzzle, moves = solver.Solve(puzzle, solver.InitPossibilities(puzzle))

	if solvedPuzzle == False: sys.exit("Puzzle Error: Puzzle is unsolvable")

	if config.PRINTSOL: IO.printSolution(solvedPuzzle)
	if config.PRINTMOV: IO.printMoves(moves)

	if config.SAVESOL: 
		if config.INPUT == "File": IO.save_solution(filename[:-4:] + "_solution.txt", solvedPuzzle)
		if config.INPUT == "Screen": IO.save_solution("screen_solution.txt", solvedPuzzle)

	if config.VISUAL:
		board = visualiser.Board(puzzle)
		board.drawMoves(moves)

if __name__ == "__main__":
	main()