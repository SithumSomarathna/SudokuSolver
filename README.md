# SudokuSolver
Processes a 9x9 Sudoku grid and returns a solution if one exists, otherwise states that it is unsolvable. Can be configured to specify various methods of inputing puzzle and outputing solution.

## Method
This solver works similar to a regular sudoku backtracking solver except it also uses inference rules to deduce if any squares on the current branch's board are guaranteed before continuing with guessing.

## config.py
Modify this to specify input and output methods.
### INPUT
	- "Screen" - Puzzle is input through UI. Press arrow keys to move input square (highlighted in green), type numbers or press backspace to add or remove values, press enter to submit. The program will notify and terminate is the submitted puzzle is invalid.
	- "File" - Puzzle is input through file. File must be a .txt file with 9 lines, each having 9 digits (no spaces). Digits 1-9 that appear corresponds to the puzzle's given value at that cell, whereas a 0 correspond to an empty cell. Upon start, the program will ask to input filename in terminal. The program will notify and terminate is the submitted puzzle is invalid. Three example inputs puzzle1.txt, puzzle2.txt and puzzle3.txt are provided.
### PRINTSOL
	- Specifies whether the solution (if one exists) should be printed to terminal.
### PRINTMOV
	- Specifies whether the order of moves performed to get to the solution (if one exists) should be printed to terminal.
### SAVESOL
	- Specifies whether the solution (if one exists) should be saved to a .txt file. The solution will be saved to "screen_solution.txt" if INPUT == "Screen" or "{filename}_solution.txt" if INPUT == "File".
### VISUAL
	- Specifies whether the visualisation of how the solution was derived (if one exists) should be displayed after solving. (Note: for puzzle that required the exploration of many branches, the visualisation may take a lot of time to display)

## Visualisation
Green represents squares that are guaranteed in the current branch's board state
Yellow represents squares that were guessed
Red represents squares that were found to have no valid entries remaining, hence terminating the current branch.
