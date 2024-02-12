import sys
import copy
import pygame
import time

class Board:

	def __init__(self, puzzle=[[0] * 9] * 9):
		self.c_white = (255,255,255)
		self.c_yellow = (252, 186, 3)
		self.c_green = (0, 212, 7)
		self.c_red = (212, 14, 0)
		self.c_black = (0, 0, 0)
		self.first = True
		
		self.thickness = 5

		pygame.init()
		pygame.font.init()
		self.font = pygame.font.SysFont('Consolas', 30)

		self.screen = pygame.display.set_mode((700, 700))
		pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80-self.thickness, 80-self.thickness, 60*9+self.thickness*2, 60*9+self.thickness*2), self.thickness)
		for i in range(9):
			for j in range(9):
				pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*j, 80+60*i, 60, 60), self.thickness)
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
			pygame.event.get()
			if type(moves[seq]) == list:
				self.first = False
				result = self.drawMov(moves[seq])
				if result == False and seq == len(moves) - 1:
					for rseq in range(len(moves)-2,-1,-1):
						if type(moves[rseq]) != list:
							pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*moves[rseq].x, 80+60*moves[rseq].y, 60, 60), self.thickness)
							pygame.draw.rect(self.screen, self.c_black, pygame.Rect(85+60*moves[rseq].x, 85+60*moves[rseq].y, 50, 50))
							self.wait(0.01)	
					return result
			else:
				if(seq == 0 and self.first == False):
					self.first == False
					self.wait(1)
					pygame.draw.rect(self.screen, self.c_yellow, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), self.thickness)
					text = self.font.render(str(moves[seq].num), True, self.c_white)
					text_rect = text.get_rect(center=(110+60*moves[seq].x, 110+60*moves[seq].y))
					self.screen.blit(text, text_rect)
					self.wait(0.05)
				elif(seq == len(moves) - 1):
					if(moves[seq].mode == 2):
						for i in range(9):
							for j in range(9):
								pygame.draw.rect(self.screen, self.c_green, pygame.Rect(80+60*j, 80+60*i, 60, 60), self.thickness)
						pygame.display.flip()
						return True
					if(moves[seq].mode == 1):
						pygame.draw.rect(self.screen, self.c_red, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), self.thickness)
						self.wait(1)
						# backtrack
						pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), self.thickness)
						self.wait(0.1)
						for rseq in range(len(moves)-2,-1,-1):
							pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*moves[rseq].x, 80+60*moves[rseq].y, 60, 60), self.thickness)
							pygame.draw.rect(self.screen, self.c_black, pygame.Rect(85+60*moves[rseq].x, 85+60*moves[rseq].y, 50, 50))
							self.wait(0.01)
						return False
				else:
					pygame.draw.rect(self.screen, self.c_green, pygame.Rect(80+60*moves[seq].x, 80+60*moves[seq].y, 60, 60), self.thickness)
					text = self.font.render(str(moves[seq].num), True, self.c_white)
					text_rect = text.get_rect(center=(110+60*moves[seq].x, 110+60*moves[seq].y))
					self.screen.blit(text, text_rect)
					self.wait(0.05)
	
	def drawMoves(self, moves):
		self.first = True
		self.drawMov(moves)
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
		pygame.quit()

	def moveCursor(self, x1, y1, x2, y2):
		pygame.draw.rect(self.screen, self.c_white, pygame.Rect(80+60*x1, 80+60*y1, 60, 60), self.thickness)
		pygame.draw.rect(self.screen, self.c_green, pygame.Rect(80+60*x2, 80+60*y2, 60, 60), self.thickness)
		
	def enterNumber(self, num, x, y, puzzle):
		if num == "": puzzle[y][x] = 0
		else: puzzle[y][x] = int(num)
		pygame.draw.rect(self.screen, self.c_black, pygame.Rect(85+60*x, 85+60*y, 50, 50))
		text = self.font.render(num, True, self.c_white)
		text_rect = text.get_rect(center=(110+60*x, 110+60*y))
		self.screen.blit(text, text_rect)
	
	def inputMoves(self, puzzle):
		running = True
		x = 0
		y = 0
		pygame.draw.rect(self.screen, self.c_green, pygame.Rect(80, 80, 60, 60), self.thickness)
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						if x > 0:
							self.moveCursor(x, y, x-1, y)
							x -= 1
					elif event.key == pygame.K_RIGHT:
						if x < 8:
							self.moveCursor(x, y, x+1, y)
							x += 1
					elif event.key == pygame.K_UP:
						if y > 0:
							self.moveCursor(x, y, x, y-1)
							y -= 1
					elif event.key == pygame.K_DOWN:
						if y < 8:
							self.moveCursor(x, y, x, y+1)
							y += 1
					elif event.unicode.isnumeric():
						if event.unicode != "0": self.enterNumber(event.unicode, x, y, puzzle)
					elif event.key == pygame.K_BACKSPACE:
						self.enterNumber("", x, y, puzzle)
					elif event.key == pygame.K_RETURN:
						running = False


			pygame.display.flip()
		pygame.quit()
        
		
	
