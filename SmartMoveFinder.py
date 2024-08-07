import random
import logging
import ChessEngineTest as ct
#White is trying to make the net sccore of the board as positive as possible and black as negative as possible
pieceScore= {"K":0 , "Q":10, "R":5, "B":3, "N":3, "p":1}
CHECKMATE=1000
STALEMATE=0
DEPTH=2


def findRandomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]


import random


def findBestMoves(gs, validMoves):
    turnMultiplier= 1 if gs.whitetoMove else -1
    opponentMinMaxScore= CHECKMATE
    bestPlayerMove= None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.MakeMove(playerMove)
        opponentMoves= gs.getValidMoves()
        if gs.checkMate:
            opponentMaxScore=-CHECKMATE
        elif gs.staleMate:
            opponentMaxScore=STALEMATE
        else:
            opponentMaxScore=-CHECKMATE
            for opponentMove in opponentMoves:
                gs.MakeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score=CHECKMATE
                elif gs.staleMate:
                    score=0
                else:
                    score = -turnMultiplier * scoreBoard(gs.board)
                if score>opponentMaxScore:
                    opponentMaxScore=score
                gs.undoMove()
        if opponentMinMaxScore>opponentMaxScore:
            opponentMaxScore=opponentMinMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

'''
Helper fundtion for the first call
'''
counter=0
def bestMoveMinMax(gs,validMoves):
    global nextMove,counter
    nextMove=None
    random.shuffle(validMoves)
    BestMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whitetoMove else -1)
    print(counter)
    return nextMove
'''
Recursive Implementation of Min Max algo
'''


def findMoveMinMax(gs, validMoves, depth, whitetoMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs)

    if whitetoMove:
        maxscore = -CHECKMATE
        for move in validMoves:
            gs.MakeMove(move)
            nextMoves = gs.getValidMoves()  # Ensure you call the method to get the moves
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxscore:
                maxscore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxscore

    else:
        minscore = CHECKMATE  # Should be CHECKMATE, not -CHECKMATE
        for move in validMoves:
            gs.MakeMove(move)
            nextMoves = gs.getValidMoves()  # Ensure you call the method to get the moves
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minscore:
                minscore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minscore


'''
Best Move based on the basis of Material
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whitetoMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score=0
    for row in gs.board:
        for square in row:
            if square[0]=='w':
                score= score+pieceScore[square[1]]
            elif square[0]=='b':
                score=score-pieceScore[square[1]]
    return score
'''
Nega Max algo
'''
def BestMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global  nextMove,count
    count=count+1
    if depth==0:
        return turnMultiplier*scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.MakeMove(move)
        nextMoves=gs.getValidMoves()
        score=-BestMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
        if score>maxScore:
            maxScore=score
            if depth==DEPTH:
                nextMove=move
        gs.undoMove()
    return maxScore

'''
Using Alpha Beta Pruning
'''
def BestMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove, counter
    counter+=1
    if depth==0:
        return turnMultiplier*scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.MakeMove(move)
        nextMoves=gs.getValidMoves()
        score=-BestMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score>maxScore:
            maxScore=score
            if depth==DEPTH:
                nextMove=move
        gs.undoMove()
        if maxScore>alpha:  #this is where pruning happens
            alpha=maxScore
        if alpha>=beta:
            break
    return maxScore






def scoreMaterial(gs):
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score = score + pieceScore[square[1]]
            elif square[0] == 'b':
                score = score - pieceScore[square[1]]
    return score