# SodukoSolver
Processes a 9x9 Soduko grid and returns a solution if one exists, otherwise states that it is unsolvable

Input:
.txt file with 9 lines, each having 9 digits (no spaces). Digits 1-9 that appear corresponds to the puzzle's given value at that cell, whereas a 0 correspond to an empty cell. Three example inputs puzzle1.txt, puzzle2.txt and puzzle3.txt are provided.

Usage:
python sudoku.py input.txt

Output:
If the puzzle has a solution, then the solution will be printed and also written to a file called input_solution.txt.
If the puzzle has no solution, then an error message will appear. 
