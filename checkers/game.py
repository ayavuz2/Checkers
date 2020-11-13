import pygame
from .constants import RED, BLUE
from checkers.board import Board


class Game:
	def __init__(self, win):
		self.win = win
		self.selected = None
		self.board = Board()
		self.turn = RED
		self.valid_moves = {}

	def update(self):
		self.board.draw(self.win)
		pygame.display.update()
