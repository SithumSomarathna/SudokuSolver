import sys
import copy

def main():
	if len(sys.argv) != 2:
		sys.exit("Usage: python sudoku.py <filename>")
	if not sys.argv[1].endswith(".txt"):
		sys.exit("File Error: Input file must be a text file")

	puzzle = []
	with open(sys.argv[1]) as f:
		contents = f.read().splitlines()
		for i in range(9):
			if len(contents[i]) != 9 or not contents[i].isnumeric(): sys.exit("File Error: Input file is not in correct format")
			puzzle.append([])
			for j in range(9):
				puzzle[i].append(int(contents[i][j]))

	solvedPuzzle = DirectSolve(FindPossibilities(puzzle))

	if solvedPuzzle == False: sys.exit("Puzzle Error: Puzzle is unsolvable")

	printSolution(solvedPuzzle)

	with open(sys.argv[1][:-4:] + "_solution.txt", 'w') as f:
		for line in solvedPuzzle:
			for number in line:
				f.write(str(number))
			f.write("\n")

def DirectSolve(poss):

	changed = True
	while changed:
		changed = CalculatePossibilities(poss)

	status = Status(poss)
	if status == 0: # Solution has been found
		return poss

	elif status == 1: # We need to guess values
		for i in range(9):
			for j in range(9):
				if type(poss[i][j]) == set:
					for x in poss[i][j]:
						newPoss = copy.deepcopy(poss)
						newPoss[i][j] = {x}
						result = DirectSolve(newPoss)
						if result != False: return result
					return False

	elif status == 2: # Puzzle is impossible
		return False

def FindPossibilities(puzzle): #Returns a matching array where each cell of the puzzle is represented with a set of possible numbers
	"""returns an array of sets corresponding to the possible values for each cell"""
	POSS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
	poss = []
	
	#Initialise Arrays
	for i in range(9):
		poss.append([])
		for j in range(9):
			if puzzle[i][j] != 0: poss[i].append(puzzle[i][j])
			else: poss[i].append(set())
	
	#find possibilities with rows
	for i in range(9):
		possRow = POSS.copy()
		for j in range(9):
			if puzzle[i][j] != 0: possRow.discard(puzzle[i][j])
		for j in range(9):
			if puzzle[i][j] == 0: poss[i][j] = possRow
	
	#print(poss)
	#find possibilities with columns
	for i in range(9):
		possCol = POSS.copy()
		for j in range(9):
			if puzzle[j][i] != 0: possCol.discard(puzzle[j][i])
		for j in range(9):
			if puzzle[j][i] == 0: poss[j][i] = poss[j][i].intersection(possCol)
			
	#print(poss)
	#find possibilities with squares
	for i in range(9):
		possSqrs = POSS.copy()
		for j in range(9):
			if puzzle[i//3*3+j//3][i%3*3+j%3] != 0: possSqrs.discard(puzzle[i//3*3+j//3][i%3*3+j%3])
		for j in range(9):
			if puzzle[i//3*3+j//3][i%3*3+j%3] == 0: poss[i//3*3+j//3][i%3*3+j%3] = poss[i//3*3+j//3][i%3*3+j%3].intersection(possSqrs)

	return poss

def UpdatePossibilities(y, x, val, poss): #Updates the possibilities array when a new value is found
	
	poss[y][x] = val
	for i in range(9):
		if type(poss[y][i]) == set:poss[y][i].discard(val)
		if type(poss[i][x]) == set:poss[i][x].discard(val)
		if type(poss[y - y%3 + i//3][x - x%3 + i%3]) == set:poss[y - y%3 + i//3][x - x%3 + i%3].discard(val)

def CalculatePossibilities(poss): #Checks if any new numbers can be guaranteed given the current position
	
	changed = False
	#Look at rows
	i = 0
	while i < 9:
		lone = False
		count = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for j in range(9):
			if type(poss[i][j]) == set:
				if len(poss[i][j]) == 1:
					UpdatePossibilities(i, j, poss[i][j].pop(), poss)
					changed = True
					lone = True
					break
				else: 
					for x in list(poss[i][j]):
						if count[x-1] == -1: count[x-1] = j
						else: count[x-1] = -2
		if lone:
			i -= 1
		else:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(i, count[x], x+1, poss)
					changed = True
		i += 1
		
	#Look at columns
	i = 0
	while i < 9:
		lone = False
		count = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for j in range(9):
			if type(poss[j][i]) == set:
				if len(poss[j][i]) == 1:
					UpdatePossibilities(j, i, poss[j][i].pop(), poss)
					changed = True
					lone = True
					break
				else: 
					for x in list(poss[j][i]):
						if count[x-1] == -1: count[x-1] = j
						else: count[x-1] = -2
		if lone:
			i -= 1
		else:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(count[x], i, x+1, poss)
					changed = True
		i += 1
		
	#Look at squares
	i = 0
	while i < 9:
		lone = False
		count = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for j in range(9):
			if type(poss[i//3*3+j//3][i%3*3+j%3]) == set:
				if len(poss[i//3*3+j//3][i%3*3+j%3]) == 1:
					UpdatePossibilities(i//3*3+j//3, i%3*3+j%3, poss[i//3*3+j//3][i%3*3+j%3].pop(), poss)
					changed = True
					lone = True
					break
				else: 
					for x in list(poss[i//3*3+j//3][i%3*3+j%3]):
						if count[x-1] == -1: count[x-1] = j
						else: count[x-1] = -2
		if lone:
			i -= 1
		else:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(i//3*3+count[x]//3, i%3*3+count[x]%3, x+1, poss)
					changed = True
		i += 1

	return changed

def Status(poss): # Returns 0 if solved, 1 if unsolved, 2 if impossible
	unsolved = False
	for i in range(9):
		for j in range(9):
			if type(poss[i][j]) == set: 
				if poss[i][j] == set(): return 2
				unsolved = True
	return 1 if unsolved else 0

def printSolution(sol):
	for i in range(9):
		if i % 3 == 0: print("+-----+-----+-----+")
		for j in range(9):
			if j % 3 == 0: print("|" + str(sol[i][j]), end="")
			else: print(" " + str(sol[i][j]), end="")
		print("|\r")
	print("+-----+-----+-----+")	

if __name__ == "__main__":
	main()