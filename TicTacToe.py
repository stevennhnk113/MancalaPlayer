from Player import *

class TTTBoard:
    def __init__(self):
        self.SIZE = 3
        self.board = [' ']*(self.SIZE*self.SIZE)
    
    def __repr__(self):
        """ Returns a string representation of the board where
            each empty square is indicated with the number of its move"""
        ret = "\n"
        for i in range(len(self.board)):
            if self.board[i] == " ":
                ret += str(i)
            else:
                ret+=self.board[i]
            if (i+1) % 3 == 0:
                ret+="\n"
        ret += "\n"
        return ret

    def legalMove( self, player, move ):
        return move in self.legalMoves(player)

    def legalMoves( self, player ):
        """ Returns the legal moves reminaing for the player in question"""
        moves = []
        for m in range( len(self.board)):
            if self.board[m] == ' ':
                moves += [m]
        return moves

    def makeMove( self, player, pos ):
        """ Make a move for player in pos.  Assumes pos is a legal move. """
        move = pos
        if move not in range(len(self.board)) or self.board[move] != ' ':
            return False
        if player.num == 1:
            self.board[move] = 'X'
        else:
            self.board[move] = 'O'
        return True
    
    def rowWin( self, c ):
        """ Has the player playing char c won in a row?"""
        for i in range(self.SIZE):
            if self.board[i*self.SIZE:(i+1)*self.SIZE] == [c]*self.SIZE:
                return True
        return False
    
    def colWin( self, c):
        """ Has the player playing char c won in a column?"""
        for i in range(self.SIZE):
            col = []
            for j in range(self.SIZE):
                col += [self.board[j*self.SIZE+i]]
                if col == [c]*self.SIZE:
                    return True
        return False
    
    def diagWin( self, c ):
        """ Has the player playing char c won in a diagonal?"""
        diag = []
        offdiag = []
        for i in range(self.SIZE):
            diag += self.board[i*self.SIZE+i]
            offdiag += self.board[((i+1)*self.SIZE)-1-i]
            if diag == [c]*self.SIZE or offdiag == [c]*self.SIZE:
                return True
        return False
    
    def hasWonPlayer( self, c ):
        """ Has the player playing c won?"""
        return self.rowWin(c) or self.colWin(c) or self.diagWin(c)
    
    def hasWon( self, playerNum ):
        """ Returns who has won: X, O, or None"""
        if playerNum == 1:
            return self.hasWonPlayer( "X" )
        else:
            return self.hasWonPlayer( "O" )

    def gameOver(self):
        """ Returns True if the game is over, and false if not"""
        if self.hasWonPlayer("X") or self.hasWonPlayer("O"):
            return True
        else:
            for move in self.board:
                if move == ' ':
                    return False
            return True
        
    def reset( self ):
        """ Reset the board for a new game """
        self.board = [' ']*(self.SIZE*self.SIZE)
        #self.board[0]='X'
        #self.board[1]='X'
        ##self.board[2]='O'
        #self.board[4]='O'

    def hostGame( self, player1, player2 ):
        """ Host a game of tic tac toe between two players"""
        self.reset()
        turn = player1      # Keep track of whose turn it is
        wait = player2
        winner = 0
        rounds = 0
        while winner == 0 and rounds < self.SIZE*self.SIZE:
            print( self )
            pos = turn.chooseMove(self)
            self.makeMove( turn, pos )
            if self.gameOver():
                if self.hasWon(turn):
                    winner = turn.num +1 %2
                elif self.hasWon(turn): winner = turn.num %2
            temp = turn
            turn = wait
            wait = temp
            rounds += 1
        print self
        if winner == 0:
            print "Tie Game"
        else:
            if winner == 1:
                print "X wins!"
            else:
                print "O wins!"

def game():
    T=TTTBoard()
    p1=Player(1,0)
    p2=Player(2,2,10)
    T.hostGame(p1,p2)
game()
