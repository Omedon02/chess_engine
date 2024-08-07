import pygame as p
import ChessEngineTest, SmartMoveFinder # Make sure this is correctly importing your ChessEngine module

# Constants
WIDTH = HEIGHT = 512
DIMENSION = 8
sq_size = WIDTH // DIMENSION
MAX_FPS = 15
Images = {}

def loadImages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        try:
            Images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sq_size, sq_size))
        except Exception as e:
            print(f"Error loading image for {piece}: {e}")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngineTest.Gamestate()
    validMoves = gs.getValidMoves()
    movemade = False  # It's a flag variable
    animate=False    #It's a flag variable to decide whether to animate or not to animate
    loadImages()
    sqSelected = ()  # This will be a tuple
    playerClicks = []  # This will be a list of tuples from starting sq to selected one
    running = True
    gameOver = False  # Initialize gameOver flag here
    playerOne=True #It will be True if its white to play and an human is playing
    playerTwo= False  #Black's place to move and false if an AI if playing otherwise for a human its True
    while running:
        humanTurn= (gs.whitetoMove and playerOne) or (not gs.whitetoMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sqSelected == (row, col):  # If the user clicked the same square twice
                        sqSelected = ()  # Deselect
                        playerClicks = []  # Clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # Append for both 1st and 2nd clicks
                    if len(playerClicks) == 2:  # After 2nd click
                        move = ChessEngineTest.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(f"Attempting move: {move.getChessNotation()}")
                        if move in validMoves:
                            gs.MakeMove(move)
                            movemade = True
                            animate=True
                            sqSelected = ()  # Reset user clicks
                            playerClicks = []
                        if not movemade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    print("Undo move")
                    gs.undoMove()
                    movemade = True
                    animate=False
                if e.key == p.K_r:   #To reset the board
                    gs= ChessEngineTest.Gamestate()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    movemade=False
                    animate=False
                    gameOver = False  # Reset gameOver flag


        #AI moves
        if not gameOver and not humanTurn:   #Its the Ai's turn to play the move
            AImoves=SmartMoveFinder.bestMoveMinMax(gs,validMoves)
            if AImoves is None:
                AImoves=SmartMoveFinder.findRandomMove(validMoves)
            gs.MakeMove(AImoves)
            movemade=True
            animate=True


        if movemade:
            if animate:
                animatedMove(gs.movelog[-1], screen, gs.board, clock)
            print("Move made, getting valid moves for the next turn")
            validMoves = gs.getValidMoves()
            movemade = False
            animate=False

        drawGameState(screen, gs, validMoves, sqSelected, gameOver)
        if gs.checkMate or gs.staleMate:
            gameOver = True  # Set gameOver flag if checkmate or stalemate
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()

def drawGameState(screen, gs, validMoves, sqSelected, gameOver):
    drawBoard(screen)
    highLightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

    if gameOver:
        if gs.checkMate:
            if gs.whitetoMove:
                drawText(screen, 'Black wins by CheckMate')
            else:
                drawText(screen, 'White wins by CheckMate')
        elif gs.staleMate:
            drawText(screen, 'StaleMate')

def highLightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        (r, c) = sqSelected
        if (gs.board[r][c][0] == 'w' and gs.whitetoMove) or (gs.board[r][c][0] == 'b' and not gs.whitetoMove):
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * sq_size, r * sq_size))
            s.fill(p.Color('yellow'))
            for m in validMoves:
                if m.startrow == r and m.startcol == c:
                    screen.blit(s, (m.endcol * sq_size, m.endrow * sq_size))

def drawBoard(screen):
    global colors
    GREEN = (118, 150, 86)
    WHITE = (238, 238, 210)
    colors = [p.Color('white'), p.Color('dark grey')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Not an empty square
                screen.blit(Images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

def animatedMove(move, screen, board, clock):
    global colors
    dR = move.endrow - move.startrow
    dC = move.endcol - move.startcol
    framesPerSquare = 10  # Number of frames per square of movement
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startrow + dR * frame / frameCount, move.startcol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endrow + move.endcol) % 2]
        endSquare = p.Rect(move.endcol * sq_size, move.endrow * sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        # When a piece is being captured
        if move.piececaptured != '--':
            screen.blit(Images[move.piececaptured], endSquare)
        # Draw the moving piece
        screen.blit(Images[move.piecemoved], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2,
        HEIGHT / 2 - textObject.get_height() / 2
    )
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()
