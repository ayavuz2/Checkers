import pygame
from .constants import RED, WHITE
from checkers.board import Board


class Game:
	def __init__(self, win):
		self.win = win
		self._init()

	def _init(self):
		self.selected = None
		self.board = Board()
		self.turn = RED
		self.valid_moves = {}

	def update(self):
		self.board.draw(self.win)
		pygame.display.update()

	def reset(self):
		self._init()

	def select(self, row, col):
		if self.selected:
			result = self._move(row, col)
			if not result:
				self.selected = None
				self.select(row, col)
		
		else:
			piece = self.board.get_piece(row, col)
			if piece != 0 and piece.color == self.turn:
				self.selected = piece
				self.valid_moves = self.board.get_valid_moves(piece)
				return True

		return False

	def _move(self, row, col):
		piece = self.board.get_piece(row, col)
		if self.selected and piece == 0 and (row, col) in self.valid_moves:
			self.board.move(self.selected, row, col)
			self.change_turn()
		else:
			return False

		return True

	def change_turn(self):
		self.turn = WHITE if self.turn == RED else RED

	def get_valid_moves(self, piece):
		moves = {}
		left = piece.col - 1
		right = piece.col + 1
		row = piece.row

		if piece.color == RED or piece.king:
			moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
			moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))

		if piece.color == WHITE or piece.king:
			moves.update(self._traverse_left(row + 1, min(row+3, ROWS), 1, piece.color, left))
			moves.update(self._traverse_right(row + 1, min(row+3, ROWS), 1, piece.color, right)) # max?

		def _traverse_left(self, start, stop, step, color, left, skipped=[]):
			moves = {}
			last = []
			for r in range(start, stop, step):
				if left < 0:
					break

				current = self.board.get_piece(r, left)
				if current == 0:
					if skipped and not last:
						break
					elif skipped:
						moves[(r, left)] = last + skipped
					else:
						moves[(r, left)] = last

					if last:
						if step == -1:
							row = max(r-3, 0)
						else:
							row = min(r+3, ROWS)

						moves.updaate(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
						moves.updaate(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
						break

				elif current.color == color:
					break
				else:
					last = [current]

				left -= 1

			return moves

		def _traverse_right(self, start, stop, step, color, right, skipped=[]):
			moves = {}
			last = []
			for r in range(start, stop, step):
				if right >= COLS:
					break

				current = self.board.get_piece(r, right)
				if current == 0:
					if skipped and not last:
						break
					elif skipped:
						moves[(r, right)] = last + skipped
					else:
						moves[(r, right)] = last

					if last:
						if step == -1:
							row = max(r-3, 0)
						else:
							row = min(r+3, ROWS)

						moves.updaate(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
						moves.updaate(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
						break

				elif current.color == color:
					break
				else:
					last = [current]

				right += 1

			return moves
