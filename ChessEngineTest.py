import logging
DIMENSION = 8

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Gamestate:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getNightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whitetoMove = True
        self.movelog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def MakeMove(self, move):
        logging.debug(f'Making move: {move.getChessNotation()}')
        self.board[move.startrow][move.startcol] = "--"
        self.board[move.endrow][move.endcol] = move.piecemoved
        self.movelog.append(move)
        self.whitetoMove = not self.whitetoMove
        if move.piecemoved == "wK":
            self.whiteKingLocation = (move.endrow, move.endcol)
        elif move.piecemoved == "bK":
            self.blackKingLocation = (move.endrow, move.endcol)
        if move.ispawnPromotion:
            self.board[move.endrow][move.endcol] = move.piecemoved[0] + 'Q'

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            logging.debug(f'Undoing move: {move.getChessNotation()}')
            self.board[move.startrow][move.startcol] = move.piecemoved
            self.board[move.endrow][move.endcol] = move.piececaptured
            self.whitetoMove = not self.whitetoMove
            if move.piecemoved == "wK":
                self.whiteKingLocation = (move.startrow, move.startcol)
            elif move.piecemoved == "bK":
                self.blackKingLocation = (move.startrow, move.startcol)

        self.checkMate=False
        self.staleMate=False

    def getValidMoves(self):
        logging.debug(f'Generating valid moves for {"white" if self.whitetoMove else "black"}')
        moves = self.getAllPossibleMoves()
        valid_moves = []
        for move in moves:
            self.MakeMove(move)
            self.whitetoMove = not self.whitetoMove
            if not self.inCheck():
                valid_moves.append(move)
            self.whitetoMove = not self.whitetoMove
            self.undoMove()
        if not valid_moves:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return valid_moves

    def inCheck(self):
        if self.whitetoMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        logging.debug(f'Checking if square ({r}, {c}) is under attack')
        self.whitetoMove = not self.whitetoMove
        opp_moves = self.getAllPossibleMoves()
        self.whitetoMove = not self.whitetoMove
        for move in opp_moves:
            if move.endrow == r and move.endcol == c:
                logging.debug(f'Square ({r}, {c}) is under attack by move: {move.getChessNotation()}')
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitetoMove) or (turn == 'b' and not self.whitetoMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    # Get all possible moves of pawn located at r, c and add it to the list
    def getPawnMoves(self, r, c, moves):
        if self.whitetoMove:  # White pawn moves
            if r - 1 >= 0 and self.board[r - 1][c] == "--":  # Move forward one square
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # Move forward two squares from starting position
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if r - 1 >= 0 and c - 1 >= 0 and self.board[r - 1][c - 1][0] == 'b':  # Capture to the left
                moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r - 1 >= 0 and c + 1 < DIMENSION and self.board[r - 1][c + 1][0] == 'b':  # Capture to the right
                moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # Black pawn moves
            if r + 1 < DIMENSION and self.board[r + 1][c] == "--":  # Move forward one square
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and r + 2 < DIMENSION and self.board[r + 2][
                    c] == "--":  # Move forward two squares from starting position
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if r + 1 < DIMENSION and c - 1 >= 0 and self.board[r + 1][c - 1][0] == 'w':  # Capture to the left
                moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r + 1 < DIMENSION and c + 1 < DIMENSION and self.board[r + 1][c + 1][0] == 'w':  # Capture to the right
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):      # writing off the Rook moves
        directions =((-1,0),(0,-1),(1,0),(0,1))
        if self.whitetoMove:
            enemycolor = "b"
        else:
            enemycolor = "w"
        for d in directions:
            for i in range(1,8):
                endrow= r + d[0]*i
                endcol= c + d[1]*i
                if 0<= endrow <=7 and 0<= endcol <=7:       #the move is on the board
                    if self.board[endrow][endcol]=="--":    #blank space
                        print("here again")
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                    elif self.board[endrow][endcol][0]==enemycolor:#enemy piece is present
                        moves.append(Move((r,c),(endrow,endcol),self.board))
                        break
                    else:   #friendly piece is present
                        break
                else:
                    break     #out of the board move

    def getNightMoves(self, r, c, moves):
        nightmoves=((-1,-2),(1,-2),(-2,-1),(-2,1),(2,-1),(2,1),(-1,2),(1,2))
        if self.whitetoMove:
            enemycolor="b"
        else:
            enemycolor="w"
        for m in nightmoves:
            endrow=r+m[0]
            endcol=c+m[1]
            if 0<=endrow<8 and 0<=endcol<8:
                if self.board[endrow][endcol]=="--" or self.board[endrow][endcol][0]==enemycolor: #empty space or enemey
                    moves.append(Move((r,c),(endrow,endcol),self.board))
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whitetoMove:
            enemycolor = "b"
        else:
            enemycolor = "w"
        for d in directions:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow <= 7 and 0 <= endcol <= 7:  # the move is on the board
                    if self.board[endrow][endcol] == "--":  # blank space
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                    elif self.board[endrow][endcol][0] == enemycolor:  # enemy piece is present
                        moves.append(Move((r, c), (endrow, endcol), self.board))
                        break
                    else:  # friendly piece is present
                        break
                else:
                    break  # out of the board move


    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
        kingmove=((-1,0),(-1,-1),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        if self.whitetoMove:
            enemycolor="b"
        else:
            enemycolor="w"
        for i in range(8):
            endrow= r + kingmove[i][0]
            endcol= c + kingmove[i][1]
            if 0<=endrow<8 and 0<=endcol<8:
                 if self.board[endrow][endcol][0]==enemycolor or self.board[endrow][endcol]=="--":
                       moves.append(Move((r,c),(endrow,endcol),self.board))

class Move:
    ranktorow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowtorank = {v: k for k, v in ranktorow.items()}
    filetocol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    coltofile = {v: k for k, v in filetocol.items()}

    def __init__(self, startsq, endsq, board):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piecemoved = board[self.startrow][self.startcol]
        self.piececaptured = board[self.endrow][self.endcol]
        self.ispawnPromotion = (self.piecemoved == 'wp' and self.endrow == 0) or (self.piecemoved == 'bp' and self.endrow == 7)

    def getChessNotation(self):
        return self.getRankfile(self.startrow, self.startcol) + self.getRankfile(self.endrow, self.endcol)

    def getRankfile(self, r, c):
        return self.coltofile[c] + self.rowtorank[r]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.startrow == other.startrow and self.startcol == other.startcol and self.endrow == other.endrow and self.endcol == other.endcol
        return False