import board
import pygame
import constants

def createTerminalGame(*args):
    #Check if the only argument is a dictionary, if so initialize the board with that dictionary

    if len(args) == 1:
        if type(args[0]) == dict:
            game = board.Board(args[0])
        elif type(args[0]) == str: # Game can be created with specific strings that correspond to default settings
            if args[0].upper() in ("BEGINNER", "INTERMEDIATE", "EXPERT"):
                game = board.Board(args[0].upper())
            else:
                print("That is not a valid preset name")
    elif len(args) == 3: # Game can be created with custom values
        game = board.Board(board.Board.createParams(args[0], args[1], args[2]))
    else:
        return
    
    game.displayTerminal() # Displays game visualied with ASCII in the terminal
    firstMove = str(input()).split(' ')
    firstMove = castIndex(firstMove) # Convert the string format input to a tuple of integers

    game.addMines(game.getMines(), firstMove) # Randomly add the mines to the board, excluding the square of the first
                                              # move to ensure that the first move is not a mine

    game.reveal([firstMove]) #Then reveal the first square guessed
    flag = True # This holds the active state of the game

    while flag:
        game.displayTerminal()
        
        index = input().split(' ')
        if len(index) == 3 and index[0].lower() == 'f': # Flag the inputted square or reveal it based on the input
                                                        # A third argument of 'f' indicates a flag request
            game.board[int(index[1])][int(index[2])].changeFlag()
        else:
            flag = game.reveal([castIndex(index)])
    
    game.displayAllTerminal()

def castIndex(index): # Converts a tuple of strings into a tuple of integers
    return (int(index[0]), int(index[1]))

#createTerminalGame("INTERMEDIATE")

def createGUIGame(*args): # Creates a visual GUI-based game
    # Load the icons used from file
    MINE_IMG = pygame.image.load(constants.MINE_PATH)
    FLAG_IMG = pygame.image.load(constants.FLAG_PATH)
    FACE_IMG = pygame.image.load(constants.FACE_PATH)

    # Same game initialisation protocol as the terminal game
    if len(args) == 1:
        if type(args[0]) == dict:
            game = board.Board(args[0])
        elif type(args[0]) == str:
            if args[0].upper() in ("BEGINNER", "INTERMEDIATE", "EXPERT"):
                game = board.Board(args[0].upper())
        else:
            print("That is not a valid preset name")
    elif len(args) == 3:
        game = board.Board(board.Board.createParams(args[0], args[1], args[2]))
    else:
        return

    # Define some values for easy access later
    rows = game.getRows()
    cols = game.getCols()

    # Dynamically calculate the required width and height of the window based on the configurations in the constants file and the inputted settings
    width = max([4*constants.SPACING+2*constants.WIDE_BUTTON_WIDTH+constants.TOP_BUTTON_HEIGHT, 2*constants.SPACING + cols*constants.SQUARE_SIZE])
    height = 2*constants.SPACING+constants.TOP_BUTTON_HEIGHT+(rows+1)*constants.SQUARE_SIZE

    # Create window with calculated dimensions
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Minesweeper")
    screen.fill(constants.BACKGROUND)

    # Define the whole counter box, the number inside the box will be handled later
    flagCounter = pygame.Rect(constants.SPACING, constants.SPACING, constants.WIDE_BUTTON_WIDTH, constants.TOP_BUTTON_HEIGHT)
    flagCounterColor = constants.BUTTON_GREY
    pygame.draw.rect(screen, flagCounterColor, flagCounter)

    # Define the restart button and render the image
    restart = pygame.Rect(int(((width-constants.TOP_BUTTON_HEIGHT)/2)), constants.SPACING, constants.TOP_BUTTON_HEIGHT, constants.TOP_BUTTON_HEIGHT)
    restartColor = constants.BUTTON_YELLOW
    pygame.draw.rect(screen, restartColor, restart)

    # Define the timer box, the exact time display will be handled later
    timer = pygame.Rect(width-constants.WIDE_BUTTON_WIDTH-constants.SPACING, constants.SPACING, constants.WIDE_BUTTON_WIDTH, constants.TOP_BUTTON_HEIGHT)
    timerColor = constants.BUTTON_GREY
    pygame.draw.rect(screen, timerColor, timer)

    # Calculate and define the required size of the box based on the size of each square and number of squares
    borderStart = (constants.SPACING - constants.SEPARATOR, constants.SPACING + constants.TOP_BUTTON_HEIGHT + constants.SQUARE_SIZE - constants.SEPARATOR)
    borderRect = pygame.Rect(   borderStart[0],
                                borderStart[1],
                                cols*constants.SQUARE_SIZE + constants.SEPARATOR,
                                rows*constants.SQUARE_SIZE + constants.SEPARATOR
    )
    borderRectColor = constants.BUTTON_GREY
    pygame.draw.rect(screen, borderRectColor, borderRect)

    baseFont = pygame.font.SysFont("Arial", 20)

    # Define all the small cells used in the game
    rectangles = [[None for c in range(cols)] for r in range(rows)]
    isRevealed = [[False for c in range(cols)] for r in range(rows)]
    for r in range(rows):
        for c in range(cols):
            rectangles[r][c] = pygame.Rect( borderStart[0] + constants.SEPARATOR + c*constants.SQUARE_SIZE,
                                            borderStart[1] + constants.SEPARATOR + r*constants.SQUARE_SIZE,
                                            constants.SQUARE_SIZE - constants.SEPARATOR,
                                            constants.SQUARE_SIZE - constants.SEPARATOR)
            pygame.draw.rect(screen, constants.HIDDEN_COLOR, rectangles[r][c])

    # Calculate the number of flags remaining and display this value in the flag counter box
    flagCounterText = baseFont.render(str(game.MINES-game.flags), True, constants.TEXT_COLOR)
    screen.blit(flagCounterText, (flagCounter[0]+constants.SPACING, flagCounter[1]+constants.SPACING))
    pygame.display.flip()

    #Display the face in the yellow box
    screen.blit(FACE_IMG, (restart[0]+constants.SEPARATOR/2, restart[1]+constants.SEPARATOR/2))

    # Display the current time
    startTime = 0
    def displayTime():
        pygame.draw.rect(screen, timerColor, timer)
        timeElapsed = pygame.time.get_ticks() - startTime if not firstReveal else 0
        timeElapsed = int(timeElapsed/1000)
        timeElapsedText = baseFont.render(str(timeElapsed), True, constants.TEXT_COLOR)
        screen.blit(timeElapsedText, (timer[0]+constants.SPACING, timer[1]+constants.SPACING))
        pygame.display.flip()




    running = True
    firstReveal = True
    while True:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit the game if the x in the corner is clicked
                    pygame.quit()
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONUP: 
                    if event.button == 1: # Left click code
                        for r in range(rows):
                            for c in range(cols):
                                # If the yellow button is pressed, a new instance of the game begins
                                if restart.collidepoint(event.pos): # Check if the restart button was clicked
                                    createGUIGame(game.getDifficulty())
                                    running = False
                                    break
                                if rectangles[r][c].collidepoint(event.pos) and not game.board[r][c].isFlag(): # Check if each square was clicked
                                    if firstReveal: # If this is the first square to be revealed, ensure a mine cannot appear there
                                        game.addMines(game.getMines(), (r, c))
                                        firstReveal = False
                                        startTime = pygame.time.get_ticks()
                                    game.reveal([(r, c)]) 
                                    if game.board[r][c].isMine(): # If it is a mine, end the game, highlighting mines red and revealing all mines
                                        for r2 in range(rows):
                                            for c2 in range(cols):
                                                if game.board[r2][c2].isMine():
                                                    pygame.draw.rect(screen, constants.MINE_COLOR, rectangles[r2][c2])
                                                    isRevealed[r2][c2] = True
                                                    screen.blit(MINE_IMG, (rectangles[r2][c2][0]+constants.SEPARATOR, rectangles[r2][c2][1]+constants.SEPARATOR))
                                        pygame.display.flip()
                                        pygame.time.wait(1000)
                                        running = False

                                    break           
                        for r in range(rows):
                            for c in range(cols):
                                if game.board[r][c].isVisible() and not isRevealed[r][c]: # Display all revealed squares
                                    isRevealed[r][c] = True
                                    pygame.draw.rect(screen, constants.REVEALED_COLOR, rectangles[r][c])
                                    if game.board[r][c].getValue() != 0 and not game.board[r][c].isMine(): # If the square has a non-zero value, display it
                                        text = baseFont.render(str(game.board[r][c].getValue()), True, constants.TEXT_COLOR)
                                        textRect = text.get_rect()
                                        textRect.center = (rectangles[r][c].centerx, rectangles[r][c].centery)
                                        screen.blit(text, textRect)
                        pygame.display.flip()
                                
                    elif event.button == 3: # Right click code
                        for r in range(rows):
                            for c in range(cols):
                                if rectangles[r][c].collidepoint(event.pos) and not game.board[r][c].isVisible():
                                    # When you right click, it flags the square, but if the square is already flagged, it unflags it
                                    if game.board[r][c].isFlag():
                                        game.board[r][c].changeFlag()
                                        pygame.draw.rect(screen, constants.HIDDEN_COLOR, rectangles[r][c])
                                        pygame.draw.rect(screen, constants.BUTTON_GREY, flagCounter)
                                        game.removeFlag()
                                        flagCounterText = baseFont.render(str(game.MINES-game.flags), True, constants.TEXT_COLOR) # Change the flag counter
                                    else:
                                        game.board[r][c].changeFlag()
                                        screen.blit(FLAG_IMG, (rectangles[r][c].x, rectangles[r][c].y))
                                        pygame.draw.rect(screen, constants.BUTTON_GREY, flagCounter)
                                        game.addFlag()
                                        flagCounterText = baseFont.render(str(game.MINES-game.flags), True, constants.TEXT_COLOR)
                                    screen.blit(flagCounterText, (flagCounter[0]+constants.SPACING, flagCounter[1]+constants.SPACING))
                                    break


                                    
                    # Check if the game is complete, if it is, stop the timer and change the color of the timer to green
                    if game.isComplete:
                        # Find the remaining mines and flag them
                        for r in range(rows):
                            for c in range(cols):
                                if game.board[r][c].isMine() and not game.board[r][c].isFlag():
                                    game.board[r][c].changeFlag()
                                    screen.blit(FLAG_IMG, (rectangles[r][c].x, rectangles[r][c].y))
                                    pygame.draw.rect(screen, constants.BUTTON_GREY, flagCounter)
                                    game.addFlag()
                                    flagCounterText = baseFont.render(str(game.MINES-game.flags), True, constants.TEXT_COLOR)
                                    screen.blit(flagCounterText, (flagCounter[0]+constants.SPACING, flagCounter[1]+constants.SPACING))
                        timerColor = constants.COMPLETE_COLOR
                        running = False
                        pygame.draw.rect(screen, timerColor, timer)
                        timeElapsed = pygame.time.get_ticks() - startTime
                        timeElapsed = int(timeElapsed/1000)
                        timeElapsedText = baseFont.render(str(timeElapsed), True, constants.TEXT_COLOR)
                        screen.blit(timeElapsedText, (timer[0]+constants.SPACING, timer[1]+constants.SPACING))


                    pygame.display.flip()
            displayTime()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if restart.collidepoint(event.pos):
                        createGUIGame(game.getDifficulty())
                        running = True
                        break
    #baseFont = pygame.font.Font(None, 20)





createGUIGame("INTERMEDIATE")





    
    
    
