import pygame
import random

# Screen sizes
width = 600
height = 400

pygame.init()
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors in RGB
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (144, 238, 144)
darkGreen = (115, 190, 115)

squareSize = 20
gameSpeed = 6 # Game tick speed
currentDirection = '' # Block the move to oposite side
pressedKeyToMove = False # Block press two or more keys at same time
pauseGame = False
foodX = 0 # food position in X
foodY = 0 # food position in Y

def generateFoodPosition():
    positionX = round(random.randrange(0, width - squareSize) / squareSize) * squareSize
    positionY = round(random.randrange(0, height - squareSize) / squareSize) * squareSize
    return positionX, positionY

def drawFood(positionX, positionY):
    pygame.draw.rect(screen, red, [positionX, positionY, squareSize, squareSize])

def drawSnake(snakePixels):
    for indice, pixel in enumerate(snakePixels):
        positionX, positionY = pixel

        lastItem = indice == (len(snakePixels) - 1)
        color = darkGreen if lastItem else green

        pygame.draw.rect(screen, color, [positionX, positionY, squareSize, squareSize])

def drawScore(score):
    font = pygame.font.SysFont("Helvetica", 15)
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, [5, 5])
        
def startGame():
    global pressedKeyToMove, foodX, foodY, pauseGame

    # Snake header position
    snakeCurrentX = width / 2
    snakeCurrentY = height / 2

    # Define how many pixels will move per tick and the direction
    directionX = 0
    directionY = 0

    snakeSize = 1
    snakePixels = []

    # Create the first food
    foodX, foodY = generateFoodPosition()

    def hasSnakeHitOwnBody():
        global pauseGame

        for pixel in snakePixels[:-1]:
            if pixel == [snakeCurrentX, snakeCurrentY]:
                pauseGame = True
                return True
        return False
    
    def hasSnakeHitTheWall():
        global pauseGame

        hasHit = snakeCurrentX < 0 or snakeCurrentX >= width or snakeCurrentY < 0 or snakeCurrentY >= height

        if hasHit: pauseGame = True

        return hasHit
    
    def updateSnakeBody():
        snakePixels.append([snakeCurrentX, snakeCurrentY])     

        if len(snakePixels) > snakeSize:
            del snakePixels[0]

    def getSnakeDirection(key):
        global currentDirection, pressedKeyToMove

        if pressedKeyToMove: return directionX, directionY

        pressedKeyToMove = True

        if key == pygame.K_DOWN and currentDirection != pygame.K_UP:
            currentDirection = pygame.K_DOWN
            return 0, squareSize

        if key == pygame.K_UP and currentDirection != pygame.K_DOWN: 
            currentDirection = pygame.K_UP
            return 0, -squareSize
        
        if key == pygame.K_LEFT and currentDirection != pygame.K_RIGHT: 
            currentDirection = pygame.K_LEFT
            return -squareSize, 0
        
        if key == pygame.K_RIGHT and currentDirection != pygame.K_LEFT: 
            currentDirection = pygame.K_RIGHT
            return squareSize, 0

        return directionX, directionY
    
    def generateFood():
        global foodX, foodY
        generateAgain = True

        while generateAgain:
            generateAgain = False

            foodX, foodY = generateFoodPosition()

            for pixel in snakePixels:
                if pixel == [foodX, foodY]: generateAgain = True

    while True:
        pressedKeyToMove = False
        stop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                stop = True
                break
            elif event.type == pygame.KEYDOWN: 
                directionX, directionY = getSnakeDirection(event.key)

        if stop: break

        screen.fill(black)

        drawFood(foodX, foodY) 

        snakeCurrentX += directionX
        snakeCurrentY += directionY

        updateSnakeBody()

        if hasSnakeHitTheWall(): break
        if hasSnakeHitOwnBody(): break

        drawSnake(snakePixels) 
        drawScore(snakeSize - 1)

        if snakeCurrentX == foodX and snakeCurrentY == foodY:
            snakeSize += 1
            generateFood()

        pygame.display.update()
        clock.tick(gameSpeed)

    while pauseGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pauseGame = False
        clock.tick(gameSpeed)

startGame()