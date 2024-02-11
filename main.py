import sys
import solver
import IO
import visualiser


def main():

	filename = input("Enter puzzle filename: ")
	puzzle = IO.load_puzzle(filename)

	solvedPuzzle, moves = solver.Solve(puzzle, solver.InitPossibilities(puzzle))

	if solvedPuzzle == False: sys.exit("Puzzle Error: Puzzle is unsolvable")

	IO.printSolution(solvedPuzzle)
	IO.printMoves(moves)

	IO.save_solution(filename[:-4:] + "_solution.txt", solvedPuzzle)

	board = visualiser.Board(puzzle)
	board.drawMoves(moves)

if __name__ == "__main__":
	main()