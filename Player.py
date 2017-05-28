# File: Player.py
# Author: 
# Date: 
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

def max(a, b):
	if a>=b:
		return a
	return b
def min(a, b):
	if a<=b:
		return a
	return b

class Player:
	""" A basic AI (or human) player """
	HUMAN = 0
	RANDOM = 1
	MINIMAX = 2
	ABPRUNE = 3
	CUSTOM = 4
	
	def __init__(self, playerNum, playerType, ply=0):	 
		self.num = playerNum
		self.opp = 2 - playerNum + 1
		self.type = playerType
		self.ply = ply

	def __repr__(self):
		return str(self.num)
		
	def minimaxMove( self, board, ply ):
		""" Choose the best minimax move.  Returns (move, val) """
		move = -1
		score = -INFINITY
		turn = self
		for m in board.legalMoves( self ):
			if ply == 0:
				return (self.score(board), m)
			if board.gameOver():
				return (-1, -1)	 # Can't make a move, the game is over
			nb = deepcopy(board)
			nb.makeMove(self, m)
			opp = Player(self.opp, self.type, self.ply)
			s, oppMove = opp.minValue(nb, ply-1, turn)
			if s > score:
				move = m
				score = s
		return score, move

	def maxValue( self, board, ply, turn):
		""" Find the minimax value for the next move for this player
			at a given board configuation
			Returns (score, oppMove)"""
		if board.gameOver():
			return (turn.score( board ), -1)
		score = -INFINITY
		move = -1
		for m in board.legalMoves( self ):
			if ply == 0:
				return (turn.score( board ), m)
			# make a new player to play the other side
			opponent = Player(self.opp, self.type, self.ply)
			# Copy the board so that we don't ruin it
			nextBoard = deepcopy(board)
			nextBoard.makeMove( self, m )
			s, oppMove = opponent.minValue(nextBoard, ply-1, turn)
			if s > score:
				move = m
				score = s
		return (score, move)
	
	def minValue( self, board, ply, turn ):
		""" Find the minimax value for the next move for this player
			at a given board configuation"""
		if board.gameOver():
			return turn.score( board ), -1
		score = INFINITY
		move = -1
		for m in board.legalMoves( self ):
			if ply == 0:
				return (turn.score( board ), m)
			# make a new player to play the other side
			opponent = Player(self.opp, self.type, self.ply)
			# Copy the board so that we don't ruin it
			nextBoard = deepcopy(board)
			nextBoard.makeMove( self, m )
			s, oppMove = opponent.maxValue(nextBoard, ply-1, turn)
			if s < score:
				score = s
				move = m
		return (score, move)


	# The default player defines a very simple score function
	# You will write the score function in the MancalaPlayer below
	# to improve on this function.
	def score(self, board):
		""" Returns the score for this player given the state of the board """
		if board.hasWon( self.num ):
			return 100.0
		elif board.hasWon( self.opp ):
			return 0.0
		else:
			return 50.0

	# You should not modify anything before this point.
	# The code you will add to this file appears below this line.

	# You will write this function (and any helpers you need)
	# You should write the function here in its simplest form:
	#	1. Use ply to determine when to stop (when ply == 0)
	#	2. Search the moves in the order they are returned from the board's
	#		legalMoves function.
	# However, for your custom player, you may copy this function
	# and modify it so that it uses a different termination condition
	# and/or a different move search order.
	def alphaBetaMove( self, board, ply ):
		""" Choose a move with alpha beta pruning """
		move = -1
		score = -INFINITY
		abScore = [-INFINITY, INFINITY]

		turn = self
		for m in board.legalMoves( self ):
			# Can't make a move, the game is over
			if board.gameOver():
				return (-1, -1)
			if ply == 0:
				return (self.score(board), m)
			
			nextABScore = deepcopy (abScore)
			nb = deepcopy(board)
			nb.makeMove(self, m)
			opp = version4(self.opp, self.type, self.ply)
			s, oppMove, a, b = opp.minValueAB(nb, ply-1, turn, nextABScore[0], nextABScore[1])
			if s > score:
				move = m
				score = s
		return score, move
		
	def maxValueAB( self, board, ply, turn, a, b):
		""" Find the minimax value for the next move for this player
		at a given board configuation
		Returns (score, oppMove)"""
			
		score = -INFINITY
		move = -1
		abScore = [a,b]
		alpha = 0
		beta = 1
		
		#a = turn.score( board )
		#print "game over returning ", turn.score( board )
		
		# print "\n This is max ", ply
		# print abScore
		
		if board.gameOver():
			# print "gameOver"
			return (turn.score( board ), -1, a, b)
		
		for m in board.legalMoves( self ):
			# print "int the loop"
			if ply == 0:
				return (self.score(board), m, a, b)
			
			nextABScore = deepcopy (abScore)
			nb = deepcopy(board)
			nb.makeMove(self, m)
			opp = version4(self.opp, self.type, self.ply)
			if score < abScore[beta]:
				s, oppMove, a, b = opp.minValueAB(nb, ply-1, turn, nextABScore[0], nextABScore[1])
				if s > score:
					move = m
					score = s
					abScore[0] = s
					# print "yes"
				#print "a ", a, " b ", b, ply
			#else:
				#print "Beta is ", abScore[beta], ", score is ", score, ", now prune ", m
		return (score, move, abScore[0], abScore[1])
	
	def minValueAB( self, board, ply, turn, a, b):
		""" Find the minimax value for the next move for this player
			at a given board configuation"""
			
		score = INFINITY
		move = -1
		abScore = [a,b]
		alpha = 0
		beta = 1
		
		#print "\n This is min ", ply 
		#print abScore
		
		if board.gameOver():
			#print "gameOver"
			return turn.score( board ), -1, a, b
		
		for m in board.legalMoves( self ):
			#print "int the loop"
			if ply == 0:
				return (self.score(board), m, a, b)
			nextABScore = deepcopy (abScore)
			nb = deepcopy(board)
			nb.makeMove(self, m)
			opp = version4(self.opp, self.type, self.ply)
			if score > abScore[0]: #index 1 is beta, if my min value is smaller than the previous alpha, i stop
				s, oppMove, a, b = opp.maxValueAB(nb, ply-1, turn, nextABScore[0], nextABScore[1])
				if s < score:
					move = m
					score = s
					abScore[beta] = s
					#print "yes"
				#print "a ", a, " b ", b, ply
			#else:
				#print "Beta is ", abScore[beta], ", score is ", score, ", now prune ", m
		return (score, move, abScore[0], abScore[1])

				
	def chooseMove( self, board ):
		""" Returns the next move that this player wants to make """
		if self.type == self.HUMAN:
			move = input("Please enter your move:")
			while not board.legalMove(self, move):
				print move, "is not valid"
				move = input( "Please enter your move" )
			return move
		elif self.type == self.RANDOM:
			move = choice(board.legalMoves(self))
			print "chose move", move, "with value", val
			return move
		elif self.type == self.MINIMAX:
			val, move = self.minimaxMove( board, self.ply )
			print "chose move", move, " with value", val
			return move
		elif self.type == self.ABPRUNE:
			val, move = self.alphaBetaMove( board, self.ply)
			print "chose move", move, " with value", val
			return move
		elif self.type == self.CUSTOM:
			# TODO: Implement a custom player
			# You should fill this in with a call to your best move choosing
			# function.	 You may use whatever search algorithm and scoring
			# algorithm you like.  Remember that your player must make
			# each move in about 10 seconds or less.
			val, move = None, None
			print "chose move", move, " with value", val
			return move
		else:
			print "Unknown player type"
			return -1


# Note, you should change the name of this player to be a custom name
# that identifies you or your team.
class version4(Player):
	""" Defines a player that knows how to evaluate a Mancala gameboard
		intelligently """

	def score(self, board):
		""" Evaluate the Mancala board for this player """
		# Currently this function just calls Player's score
		# function.	 You should replace the line below with your own code
		# for evaluating the board
		""" Returns the score for this player given the state of the board """
		if board.hasWon( self.num ):
			return 100.0
		elif board.hasWon( self.opp ):
			return 0.0
		else:
			# 2 points if:	there is a play that can land on zero spot where
							# where the opposite spot has something
			score = 0
			if(self.num == 0):
				mySpots = board.P1Cups
				oppSpots = board.P2Cups
			else:
				mySpots = board.P2Cups
				oppSpots = board.P1Cups
			
			#Account for the number of empty spots, more empty spot is better
			
			# emtpy_spot_index is the index of the empty spot
			for emtpy_spot_index in range(len(mySpots)):
				if mySpots[emtpy_spot_index] == 0 and oppSpots[emtpy_spot_index] > 0:
					for findingIndex in range(0, emtpy_spot_index):
						if mySpots[findingIndex] == emtpy_spot_index - findingIndex:
							score = score + 2*oppSpots[emtpy_spot_index]
			
			#Less empty spots on the opp side will better
			for emtpy_spot_index in range(len(oppSpots)):
				if oppSpots[emtpy_spot_index] != 0:
					score = score + 2
					
			#Dont give the opp the second chance
						
			spot_till_mancala = 6	#The beginning spot has to take 6 moves
									# before they hit the mancala
			for spot in mySpots:
				if spot > spot_till_mancala:
					score = score + 1
				elif spot == spot_till_mancala:
					score = score + 2
				spot_till_mancala = spot_till_mancala - 1
				
			# for spot in mySpots:
				# if spot > spot_till_mancala:
					# score = score + 1
				# elif spot == spot_till_mancala:
					# nb = deepcopy(board)
					# nb.makeMove(self, mySpots.index(spot))
					# score = self.score(nb)
				# spot_till_mancala = spot_till_mancala - 1
			
			return score

	   




