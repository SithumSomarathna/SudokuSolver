import sys
import copy
import pygame
import time

class Move:

	def __init__(self, x, y, num, mode):
		self.x = x
		self.y = y
		self.num = num
		self.mode = mode # 0: a number was placed here, 1: this cell had no possibilities, 2: puzzle is solved

class Board:

	def __init__(self, puzzle):
		self.c_white = (255,255,255)
		self.c_yellow = (252, 186, 3)
		self.c_green = (0, 212, 7)
		self.c_red = (212, 14, 0)
		self.c_black = (0, 0, 0)
		self.first = True

		pygame.init()
		pygame.font.init()
		self.font = pygame.font.SysFont('Arial', 30)

		self.screen = pygame.display.set_mode((700, 700))
		for i in range(9):
			for j in range(9):
				pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*j, 80+60*i, 60, 60), 2)
				if puzzle[i][j] != 0:
					text = self.font.render(str(puzzle[i][j]), True, self.c_white)
					text_rect = text.get_rect(center=(110+60*j, 110+60*i))
					self.screen.blit(text, text_rect)
		
		pygame.display.flip()

	def wait(self, t):
		pygame.display.flip()
		time.sleep(t)

	def drawMov(self, moves):
		for seq in range(len(moves)):
			if type(moves[seq]) == list:
				self.first = False
				result = self.drawMov(moves[seq])
				if result == False and seq == len(moves) - 1:
					for rseq in range(len(moves)-2,-1,-1):
						if type(moves[rseq]) != list:
							pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*moves[rseq].x, 80+60*moves[rseq].y, 60, 60), 2)
							pygame.draw.rect(self.screen, self.c_black, pygame.Rect(85+60*moves[rseq].x, 85+60*moves[rseq].y, 50, 50))
							self.wait(0.01)	
					return result
			else:
				if(seq == 0 and self.first == False):
					self.first == False
					self.wait(1)
					pygame.draw.rect(self.screen, self.c_yellow, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), 2)
					text = self.font.render(str(moves[seq].num), True, self.c_white)
					text_rect = text.get_rect(center=(110+60*moves[seq].x, 110+60*moves[seq].y))
					self.screen.blit(text, text_rect)
					self.wait(0.05)
				elif(seq == len(moves) - 1):
					if(moves[seq].mode == 2):
						for i in range(9):
							for j in range(9):
								pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*j, 80+60*i, 60, 60), 2)
						self.wait(4)
						return True
					if(moves[seq].mode == 1):
						pygame.draw.rect(self.screen, self.c_red, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), 2)
						self.wait(1)
						# backtrack
						pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), 2)
						self.wait(0.1)
						for rseq in range(len(moves)-2,-1,-1):
							pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*moves[rseq].x, 80+60*moves[rseq].y, 60, 60), 2)
							pygame.draw.rect(self.screen, self.c_black, pygame.Rect(85+60*moves[rseq].x, 85+60*moves[rseq].y, 50, 50))
							self.wait(0.01)
						return False
				else:
					pygame.draw.rect(self.screen, self.c_green, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), 2)
					text = self.font.render(str(moves[seq].num), True, self.c_white)
					text_rect = text.get_rect(center=(110+60*moves[seq].x, 110+60*moves[seq].y))
					self.screen.blit(text, text_rect)
					self.wait(0.05)
	
	def drawMoves(self, moves):
		self.first = True
		self.drawMov(moves)

def printMoves(moves):
	print("\n")
	for seq in moves:
		if type(seq) == list:
			printMoves(seq)
		else:
			print("Move {(" + str(seq.x) + ", " + str(seq.y) + ") " + str(seq.num) + " " + str(seq.mode) + "}")

def main():
	# Validate inputs 
	if len(sys.argv) != 2:
		sys.exit("Usage: python sudokuVisual.py <filename>")
	if not sys.argv[1].endswith(".txt"):
		sys.exit("File Error: Input file must be a text file")

	# Read inputs
	puzzle = []
	with open(sys.argv[1]) as f:
		contents = f.read().splitlines()
		for i in range(9):
			if len(contents[i]) != 9 or not contents[i].isnumeric(): sys.exit("File Error: Input file is not in correct format")
			puzzle.append([])
			for j in range(9):
				puzzle[i].append(int(contents[i][j]))

	moves = []
	solvedPuzzle = DirectSolve(FindPossibilities(puzzle), moves)

	board = Board(puzzle)
	board.drawMoves(moves)

	if solvedPuzzle == False: sys.exit("Puzzle Error: Puzzle is unsolvable")

	printSolution(solvedPuzzle)

	# Write output
	with open(sys.argv[1][:-4:] + "_solution.txt", "w") as f:
		for line in solvedPuzzle:
			for number in line:
				f.write(str(number))
			f.write("\n")

def DirectSolve(poss, moves):

	changed = True
	while changed:
		changed = CalculatePossibilities(poss, moves)

	status = Status(poss, moves)
	if status == 0: # Solution has been found
		return poss

	elif status == 1: # We need to guess values
		for i in range(9):
			for j in range(9):
				if type(poss[i][j]) == set:
					for x in poss[i][j]:
						newPoss = copy.deepcopy(poss)
						newPoss[i][j] = {x}
						newMoves = []
						result = DirectSolve(newPoss, newMoves)
						moves.append(newMoves)
						if result != False: return result
					return False

	elif status == 2: # Puzzle is impossible
		return False

def FindPossibilities(puzzle): #Returns a matching array where each cell of the puzzle is represented with a set of possible numbers
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

def UpdatePossibilities(y, x, val, poss): #Updates the possibilities array when a new value is found
	
	poss[y][x] = val
	for i in range(9):
		if type(poss[y][i]) == set: poss[y][i].discard(val)
		if type(poss[i][x]) == set: poss[i][x].discard(val)
		if type(poss[y - y%3 + i//3][x - x%3 + i%3]) == set: poss[y - y%3 + i//3][x - x%3 + i%3].discard(val)

def CalculatePossibilities(poss, moves): #Checks if any new numbers can be guaranteed given the current position
	
	changed = False
	#Look at rows
	i = 0
	while i < 9:
		lone = False
		count = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for j in range(9):
			if type(poss[i][j]) == set:
				if len(poss[i][j]) == 1:					# Check if there's only one possible value in a cell
					num = poss[i][j].pop()
					UpdatePossibilities(i, j, num, poss)
					moves.append(Move(j, i, num, 0))
					changed = True
					lone = True
					break
				else: 
					for x in list(poss[i][j]):				# Check if there is a number that is possible in only one cell of the row
						if count[x-1] == -1: count[x-1] = j
						else: count[x-1] = -2
		if lone:
			i -= 1
		else:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(i, count[x], x+1, poss)
					moves.append(Move(count[x], i, x+1, 0))
					changed = True
					break
		i += 1
		
	#Look at columns
	i = 0
	while i < 9:
		lone = False
		count = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for j in range(9):
			if type(poss[j][i]) == set:
				if len(poss[j][i]) == 1:					# Check if there's only one possible value in a cell
					num = poss[j][i].pop()
					UpdatePossibilities(j, i, num, poss)
					moves.append(Move(i, j, num, 0))
					changed = True
					lone = True
					break
				else: 
					for x in list(poss[j][i]):				# Check if there is a number that is possible in only one cell of the column
						if count[x-1] == -1: count[x-1] = j
						else: count[x-1] = -2
		if lone:
			i -= 1
		else:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(count[x], i, x+1, poss)
					moves.append(Move(i, count[x], x+1, 0))
					changed = True
					break
		i += 1
		
	#Look at squares
	i = 0
	while i < 9:
		lone = False
		count = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		for j in range(9):
			if type(poss[i//3*3+j//3][i%3*3+j%3]) == set:
				if len(poss[i//3*3+j//3][i%3*3+j%3]) == 1:	# Check if there's only one possible value in a cell
					num = poss[i//3*3+j//3][i%3*3+j%3].pop()
					UpdatePossibilities(i//3*3+j//3, i%3*3+j%3, num, poss)
					moves.append(Move(i%3*3+j%3, i//3*3+j//3, num, 0))
					changed = True
					lone = True
					break
				else: 
					for x in list(poss[i//3*3+j//3][i%3*3+j%3]): # Check if there is a number that is possible in only one cell of the sqaure
						if count[x-1] == -1: count[x-1] = j
						else: count[x-1] = -2
		if lone:
			i -= 1
		else:
			for x in range(9):
				if count[x] >= 0:
					UpdatePossibilities(i//3*3+count[x]//3, i%3*3+count[x]%3, x+1, poss)
					moves.append(Move(i%3*3+count[x]%3, i//3*3+count[x]//3, x+1, 0))
					changed = True
					break
		i += 1

	return changed

def Status(poss, moves): # Returns 0 if solved, 1 if unsolved, 2 if impossible
	unsolved = False
	for i in range(9):
		for j in range(9):
			if type(poss[i][j]) == set: 
				if poss[i][j] == set(): # There is a cell with no possibilities, hence unsolvable
					moves.append(Move(j, i, None, 1))
					return 2 
				unsolved = True	# There is a cell with multiple possibilities, hence unsolved
	if unsolved: return 1
	else:
		moves.append(Move(None, None, None, 2))
		return 0

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