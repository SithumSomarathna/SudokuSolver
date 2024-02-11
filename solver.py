import copy

class Move:
	def __init__(self, x, y, num, mode):
		self.x = x
		self.y = y
		self.num = num
		self.mode = mode # 0: a number was placed here, 1: this cell had no possibilities, 2: puzzle is solved
		
	def __repr__(self):
		if self.mode == 0: return f"{self.num} was placed at ({self.x}, {self.y})"
		if self.mode == 1: return f"({self.x}, {self.y}) has no valid numbers"
		if self.mode == 2: return "The puzzle is solved"

def InitPossibilities(puzzle): #Returns a matching array where each cell of the puzzle is represented with a set of possible numbers

	POSS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
	poss = []
	for i in range(9):
		poss.append([])
		for j in range(9):
			poss[i].append(set())
	
	#find possibilities with rows
	for i in range(9):
		possRow = POSS.copy()
		for j in range(9):
			if puzzle[i][j] != 0: possRow.discard(puzzle[i][j])
		for j in range(9):	
			if puzzle[i][j] == 0:
				poss[i][j] = possRow	
	
	#find possibilities with columns
	for i in range(9):
		possCol = POSS.copy()
		for j in range(9):
			if puzzle[j][i] != 0: possCol.discard(puzzle[j][i])
		for j in range(9):
			if puzzle[j][i] == 0: poss[j][i] = poss[j][i].intersection(possCol)
			
	#find possibilities with squares
	for i in range(9):
		possSqrs = POSS.copy()
		for j in range(9):
			if puzzle[i//3*3+j//3][i%3*3+j%3] != 0: possSqrs.discard(puzzle[i//3*3+j//3][i%3*3+j%3])
		for j in range(9):
			if puzzle[i//3*3+j//3][i%3*3+j%3] == 0: poss[i//3*3+j//3][i%3*3+j%3] = poss[i//3*3+j//3][i%3*3+j%3].intersection(possSqrs)

	return poss

def UpdatePossibilities(y, x, val, poss, puzzle): #Updates the possibilities array when a new value is found
	
	puzzle[y][x] = val
	poss[y][x] = set()
	for i in range(9):
		poss[y][i].discard(val)
		poss[i][x].discard(val)
		poss[y - y%3 + i//3][x - x%3 + i%3].discard(val)

def FindImplications(puzzle, poss, moves): #Checks if any new numbers can be guaranteed given the current position
	
	changed = False
	#Look at rows
	for i in range(9):
		lone = False
		count = [-1] * 9  # counts how many times a number is seen in total - -1: Never seen, j: Seen once and in position j, -2: Seen more than once 
		for j in range(9):
			if len(poss[i][j]) == 1:
				num = poss[i][j].pop()
				UpdatePossibilities(i, j, num, poss, puzzle)
				moves.append(Move(j, i, num, 0))
				changed = True
				lone = True
				break
			else: 
				for x in list(poss[i][j]):
					if count[x-1] == -1: count[x-1] = j
					else: count[x-1] = -2

		if not lone:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(i, count[x], x+1, poss, puzzle)
					moves.append(Move(count[x], i, x+1, 0))
					changed = True
					break
		
	#Look at columns
	for i in range(9):
		lone = False
		count = [-1] * 9
		for j in range(9):
			if len(poss[j][i]) == 1:
				num = poss[j][i].pop()
				UpdatePossibilities(j, i, num, poss, puzzle)
				moves.append(Move(i, j, num, 0))
				changed = True
				lone = True
				break
			else: 
				for x in list(poss[j][i]):
					if count[x-1] == -1: count[x-1] = j
					else: count[x-1] = -2
		if not lone:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(count[x], i, x+1, poss, puzzle)
					moves.append(Move(i, count[x], x+1, 0))
					changed = True
					break
		
	#Look at squares
	for i in range(9):
		lone = False
		count = [-1] * 9
		for j in range(9):
			if len(poss[i//3*3+j//3][i%3*3+j%3]) == 1:
				num = poss[i//3*3+j//3][i%3*3+j%3].pop()
				UpdatePossibilities(i//3*3+j//3, i%3*3+j%3, num, poss, puzzle)
				moves.append(Move(i%3*3+j%3, i//3*3+j//3, num, 0))
				changed = True
				lone = True
				break
			else: 
				for x in list(poss[i//3*3+j//3][i%3*3+j%3]):
					if count[x-1] == -1: count[x-1] = j
					else: count[x-1] = -2
		if not lone:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(i//3*3+count[x]//3, i%3*3+count[x]%3, x+1, poss, puzzle)
					moves.append(Move(i%3*3+count[x]%3, i//3*3+count[x]//3, x+1, 0))
					changed = True
					break

	return changed

def Status(puzzle, poss, moves): # Returns 0 if solved, 1 if unsolved, 2 if impossible
	unsolved = False
	for i in range(9):
		for j in range(9):
			if puzzle[i][j] == 0: 
				if poss[i][j] == set(): 
					moves.append(Move(j, i, None, 1))
					return 2
				unsolved = True
	if unsolved: return 1
	else:
		moves.append(Move(None, None, None, 2))
		return 0

def Solve(puzzle, poss):

	moves = []
	
	changed = True
	while changed:
		changed = FindImplications(puzzle, poss, moves)

	status = Status(puzzle, poss, moves)

	if status == 0: # Solution has been found
		return puzzle, moves

	elif status == 1: # We need to guess values
		for i in range(9):
			for j in range(9):
				if puzzle[i][j] == 0:
					for x in poss[i][j]:
						newPoss = copy.deepcopy(poss)
						newPoss[i][j] = {x}
						newPuzzle = copy.deepcopy(puzzle)
						result, newMoves = Solve(newPuzzle, newPoss)
						moves.append(newMoves)
						if result != False: return result, moves
					return False, moves

	elif status == 2: # Puzzle is impossible
		return False, moves