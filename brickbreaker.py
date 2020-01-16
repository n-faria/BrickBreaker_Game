import math, pygame, random, time

# Call this function so the Pygame library can initialize itself
pygame.init()

###COLOURS###
grey = (195, 195, 195)
darkgrey = (150, 150, 150)
white = (210, 210, 210)
black = (0, 0, 0)

###IMAGES###

#Arrow Keys

leftArrow = pygame.image.load("leftarrow.png")
leftArrowKey = pygame.transform.scale(leftArrow, (75, 75))

rightArrow = pygame.image.load("rightarrow.png")
rightArrowKey = pygame.transform.scale(rightArrow, (75, 75))

#Platform
platformImage = pygame.image.load("platform.png")
platformEnlarged = pygame.transform.scale(platformImage, (142, 30))

#Ball
ball = pygame.image.load("ball.png")
ballImage = pygame.transform.scale(ball,(25,25))
ballImageEnlarged = pygame.transform.scale(ball,(75,75))

#Horizontal Border
horizontalBorder = pygame.image.load("cautiontape.png")
borderImageH = pygame.transform.scale(horizontalBorder, (1152, 25))

#Vertical Border
verticalBorder = pygame.image.load("caution_tape.png")
borderImageV = pygame.transform.scale(verticalBorder, (25, 832))

#Metal Brick
metalBrick = pygame.image.load("metalbrick.png")
metalBrickImage = pygame.transform.scale(metalBrick, (128, 64))

#Brick
brick = pygame.image.load("brick.png")
brickImage = pygame.transform.scale(brick, (128, 64))

###SOUNDS###
collision_sound = pygame.mixer.Sound("bump.wav")
pygame.mixer.music.load("backgroundmusic.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

###################################################################################################CLASSES####################################################################################################

#BALL CLASS

class Ball(pygame.sprite.Sprite):
 
    def __init__(self):

        super().__init__()
 
        self.image = ballImage #Sets the sprites image

        #Get the screen width and height for reference
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection

        #Get the center of the rect
        self.center = self.rect.center

        #Create variables for the x coordinate and y coordinate of the center
        self.centerx = self.center[0]
        self.centery = self.center[1]

        #Starting point for the rect of the image on the screen
        self.rect.x = 0.485 * self.screenwidth
        self.rect.y = 0.85 * self.screenheight

        #Creates 2 variables for the x speed and y speed of the ball
        self.speedx = 0
        self.speedy = 0

        # Direction of ball in degrees
        self.direction = 0
 
        self.reset() #Puts the ball at its starting point
 
    def reset(self):
        #Put the rect of the ball back to its starting position
        self.x = self.screenwidth * 0.485
        self.y = self.screenheight * 0.85
        
        #Make the speed of the ball equal to 10
        self.speedx = 10
        self.speedy = 10

        #Choose a random direction for the ball to shoot out at
        self.direction = random.randrange(-75, 75)
 
    # Updates the ball
    def update(self):
        
        # Sine and Cosine work in degrees, so they have to be converted
        direction_radians = math.radians(self.direction)
 
        # Change the position (x and y) according to the speed and direction
        self.x += self.speedx * math.sin(direction_radians)
        self.y -= self.speedy * math.cos(direction_radians)
 
        if self.y > 832: #If the ball falls below the screen

            #Reset the ball and player positions
            self.reset()
            player.playerReset()
            
            #Update the player's lives to -1
            player.lives -= 1

            #Check if the player has any lives left
            if player.lives == 0:
                gameLose() #If they don't, then take them to the losing screen

            else: #Otherwise, they arre still playing
                
                #Draw the you lost a life screen
                mediumText = pygame.font.Font("techno_hideo.ttf", 100)
                textSurf, textRect = text_objects("You Lost a Life!",mediumText)
                textRect.center = ((screenwidth / 2), (screenheight * 0.3))
                screen.blit(textSurf, textRect)
                smallerText = pygame.font.Font("techno_hideo.ttf", 50)
                livesMessage = "Lives Remaining: " + str(player.lives)
                textSurf, textRect = text_objects(livesMessage, smallerText)
                textRect.center = ((screenwidth / 2), (screenheight * 0.5))
                screen.blit(textSurf, textRect)
                
                pygame.display.update() #Update display
                time.sleep(4) #Wait for 4 seconds

 
        # Move the image to where the new x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 

#PLATFORM CLASS

class Player(pygame.sprite.Sprite):
    
    def __init__(self):

        super().__init__()
        
        self.image = platformImage #Sets the sprites image
 
        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection
        
        #Get the screen width and height for reference
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.lives = 3 #Sets player's lives to 3
        self.score = 0 #Sets player's score to 0

        #Puts the platform rect at its starting position
        self.rect.x = 0.475 * self.screenwidth 
        self.rect.y = 0.9 * self.screenheight
 
    def playerReset(self): #Resets the platform to its original position
        self.rect.x = 0.435 * self.screenwidth
        self.rect.y = 0.9 * self.screenheight
    
    def move(self, dx, dy):
        
        # Move each axis separately if dx or dy have a value (if the platform has been moved)
        if dx != 0:
            self.Update(dx, 0)
        if dy != 0:
            self.Update(0, dy)
    
    def Update(self, dx, dy):
        
        #Move the rect to its new location
        self.rect.x += dx
        self.rect.y += dy
 
        # Make sure the platform doesn't go past the borders
        if self.rect.right > self.screenwidth - 25:
            self.rect.right = self.screenwidth - 25
        if self.rect.left < 25:
            self.rect.left = 25

#NEXT 3 CLASSES ARE FOR THE OUTSIDE BORDERS

class hBorder(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = borderImageH #Sets the sprites image

        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection

        #Put the rect of the image where it needs to be
        self.rect.x = 0
        self.rect.y = 0

class VBorder_L(pygame.sprite.Sprite):
    
    def __init__(self):

        super().__init__()

        self.image = borderImageV #Sets the sprites image

        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection

        #Put the rect of the image where it needs to be
        self.rect.x = 0
        self.rect.y = 0

class VBorder_R(pygame.sprite.Sprite):
    
    def __init__(self):

        super().__init__()

        self.screenwidth = pygame.display.get_surface().get_width()

        self.image = borderImageV #Sets the sprites image

        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection

        #Put the rect of the image where it needs to be
        self.rect.x = self.screenwidth - 25
        self.rect.y = 0

class MetalBrick(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = metalBrickImage #Sets the sprites image

        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection

    def display(self, position):

        #Sets two variables to equal the x and y coordinates passed on by the list of positions from the tilemap
        self.x = position[0]
        self.y = position[1]

        #Rects the image at the position coordinates
        self.rect.x = self.x
        self.rect.y = self.y

class Brick(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = brickImage #Sets the sprites image

        self.rect = self.image.get_rect() #Create a rectangle around the image for collision detection

    def display(self, position):

        #Sets two variables to equal the x and y coordinates passed on by the list of positions from the tilemap
        self.x = position[0]
        self.y = position[1]

        #Rects the image at the position coordinates
        self.rect.x = self.x
        self.rect.y = self.y

########################################################################################################SCREENS###############################################################################################

#Function used to display text
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#INTRO SCREEN
def gameIntro():
    
    pygame.mixer.music.play(-1) #Play the background music
    exit_program = False
    
    while not exit_program:
        #If quit, quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
                pygame.quit()
                quit()
                
            screen.fill(grey) #Fill the screen with the background colour

            #Get positions of the mouse and mouse click
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            ###BUTTONS###


            #QUIT BUTTON
            if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 600 + 40 > mouse[1] > 600: #If the mouse is over the button, draw a lighter version
                pygame.draw.rect(screen, black, (screenwidth/2 - 250, 600, 500, 60))
                pygame.draw.rect(screen, white, (screenwidth/2 - 240, 610, 480, 40))
                if click[0] == 1: #If they press the button, quit pygame
                    pygame.quit()   
            else:
                pygame.draw.rect(screen, black, (screenwidth/2 - 250, 600, 500, 60))
                pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 610, 480, 40))
            
                
            #INSTRUCTIONS BUTTON
            if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 530 + 40 > mouse[1] > 530: #If the mouse is over the button, draw a lighter version
                pygame.draw.rect(screen, black, (screenwidth/2 - 250, 530, 500, 60))
                pygame.draw.rect(screen, white, (screenwidth/2 - 240, 540, 480, 40))
                if click[0] == 1: #If they press the button, go to the instructions screen
                    gameInstructions()
            else:
                pygame.draw.rect(screen, black, (screenwidth/2 - 250, 530, 500, 60))
                pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 540, 480, 40))

            
            #PLAY GAME BUTTON
            if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 460 + 40 > mouse[1] > 460: #If the mouse is over the button, draw a lighter version
                pygame.draw.rect(screen, black, (screenwidth/2 - 250, 460, 500, 60))
                pygame.draw.rect(screen, white, (screenwidth/2 - 240, 470, 480, 40))
                if click[0] == 1: #If they press the button, run the game loop
                    gameLoop()
            else:
                pygame.draw.rect(screen, black, (screenwidth/2 - 250, 460, 500, 60))
                pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 470, 480, 40))

            
            #Creates the fonts
            smallText = pygame.font.Font("techno_hideo.ttf", 30)
            bigText = pygame.font.Font("techno_hideo.ttf", 150)

            #Displays the Play Game text
            textSurf, textRect = text_objects("Play Game", smallText)
            textRect.center = ((screenwidth/2), (470 + 20))
            screen.blit(textSurf, textRect)

            #Displays the Instructions text
            textSurf, textRect = text_objects("Instructions", smallText)
            textRect.center = ((screenwidth/2), (540 + 20))
            screen.blit(textSurf, textRect)

            #Displays the Quit text
            textSurf, textRect = text_objects("Quit", smallText)
            textRect.center = ((screenwidth/2), (610 + 20))
            screen.blit(textSurf, textRect)

            #Displays the title
            
            textSurf, textRect = text_objects("Nick's Bricks", bigText)
            textRect.center = ((screenwidth / 2), (screenheight * 0.3))
            screen.blit(textSurf, textRect)
            
            pygame.display.update() #Updates display
            clock.tick(30) #FPS to 30

#INSTRUCTIONS SCREEN
def gameInstructions():
    
    exit_program = False
    
    while not exit_program:
        #If quit, quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
                pygame.quit()
                quit()
                
            screen.fill(grey) #Fill the screen with the background colour

            #Get positions of the mouse and mouse click
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            #Creates the fonts
            smallText = pygame.font.Font("techno_hideo.ttf", 20)
            medText = pygame.font.Font("techno_hideo.ttf", 30)

            ###DISPLAY###
            
            #DRAWS PLATFORM STUFF
            pygame.draw.rect(screen, black, (90, 90, 620, 180))
            pygame.draw.rect(screen, darkgrey, (100, 100, 600, 160))
            screen.blit(platformEnlarged, (875, 170))
            screen.blit(leftArrowKey, (287, 175))
            screen.blit(rightArrowKey, (437, 175))
            textSurf, textRect = text_objects("Move the platform with the arrow keys.", smallText)
            textRect.center = ((400), (130))
            screen.blit(textSurf, textRect)

            #DRAWS BALL STUFF
            pygame.draw.rect(screen, black, (90, 290, 620, 180))
            pygame.draw.rect(screen, darkgrey, (100, 300, 600, 160))
            textSurf, textRect = text_objects("Bounce the ball off the platform.", smallText)
            textRect.center = ((400), (342))
            screen.blit(textSurf, textRect)
            textSurf, textRect = text_objects("If it falls below the platform, you lose a life.", smallText)
            textRect.center = ((400), (405))
            screen.blit(textSurf, textRect)
            screen.blit(ballImageEnlarged, (912, 335))


            #DRAWS BRICKS STUFF
            pygame.draw.rect(screen, black, (90, 490, 620, 180))
            pygame.draw.rect(screen, darkgrey, (100, 500, 600, 160))
            textSurf, textRect = text_objects("Break the normal bricks to gain points.", smallText)
            textRect.center = ((400), (542))
            screen.blit(textSurf, textRect)
            textSurf, textRect = text_objects("Metal bricks cannot be broken.", smallText)
            textRect.center = ((400), (605))
            screen.blit(textSurf, textRect)
            screen.blit(brickImage, (880, 512))
            screen.blit(metalBrickImage,(880, 589))

            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 700, 500, 60))
            pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 710, 480, 40))
            textSurf, textRect = text_objects("Break all the bricks to win!", smallText)
            textRect.center = ((screenwidth/2), (710 + 20))
            screen.blit(textSurf, textRect)

            #DRAWS BACK BUTTON STUFF
            if 0 + 170 > mouse[0] > 0 and 770 + 70 > mouse[1] > 770: #If the mouse is over the button, display a lighter version
                pygame.draw.rect(screen, black, (0, 770, 170, 70))
                pygame.draw.rect(screen, white, (0, 780, 160, 60))
                if click[0] == 1:
                    gameIntro() #If they click back, go back to the intro screen
            else:
                pygame.draw.rect(screen, black, (0, 770, 170, 70))
                pygame.draw.rect(screen, darkgrey, (0, 780, 160, 60))

            #Back button text
            textSurf, textRect = text_objects("Back", medText)
            textRect.center = ((75), (807))
            screen.blit(textSurf, textRect)
            
            pygame.display.update() #Updates display
            clock.tick(30) #FPS to 30
    
#LOSING SCREEN           
def gameLose():
    
    pygame.mixer.music.stop() #Stop the background music
    pygame.mixer.Sound.play(gameover_sound) #Play the game over sound
   
    exit_program = False
    
    while not exit_program:
        #If quit, quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
                pygame.quit()
                
        screen.fill(grey) #Fill the screen with the background colour

        #Get positions of the mouse and mouse click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        #Fonts
        bigText = pygame.font.Font("techno_hideo.ttf", 150)
        mediumText = pygame.font.Font("techno_hideo.ttf", 90)
        smallText = pygame.font.Font("techno_hideo.ttf", 30)
        
        ###BUTTONS###

        #QUIT BUTTON
        if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 600 + 40 > mouse[1] > 600: #If the mouse is over the button, display a lighter version  
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 600, 500, 60))
            pygame.draw.rect(screen, white, (screenwidth/2 - 240, 610, 480, 40))
            if click[0] == 1: #If they click the quit button, quit
                pygame.quit()
        else:
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 600, 500, 60))
            pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 610, 480, 40))

        #RETRY BUTTON
        if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 530 + 40 > mouse[1] > 530: #If the mouse is over the button, display a lighter version
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 530, 500, 60))
            pygame.draw.rect(screen, white, (screenwidth/2 - 240, 540, 480, 40))
            if click[0] == 1: #If they click the retry button, restart the game loop
                gameLoop()
        else:
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 530, 500, 60))
            pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 540, 480, 40))

        #Text on the Retry button
        textSurf, textRect = text_objects("Retry", smallText)
        textRect.center = ((screenwidth/2), (540 + 20))
        screen.blit(textSurf, textRect)

        #Text on the Quit button
        textSurf, textRect = text_objects("Quit", smallText)
        textRect.center = ((screenwidth/2), (610 + 20))
        screen.blit(textSurf, textRect)

        #You lose text
        textSurf, textRect = text_objects("You Lose!", bigText)
        textRect.center = ((screenwidth / 2), (screenheight * 0.3))
        screen.blit(textSurf, textRect)

        #Score text
        losingMessage = "Score: " + str(player.score * 100)
        textSurf, textRect = text_objects(losingMessage, mediumText)
        textRect.center = ((screenwidth / 2), (screenheight * 0.5))
        screen.blit(textSurf, textRect)
        
        pygame.display.update() #Update display
        clock.tick(30) #FPS to 30


#WIN SCREEN
def gameWin():
    
    exit_program = False
    
    while not exit_program:
        #If quit, quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True
                pygame.quit()
                
        screen.fill(grey) #Fill the screen with the background colour

        #Get positions of the mouse and mouse click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #FONTS
        medText = pygame.font.Font("techno_hideo.ttf", 100)
        mediumText = pygame.font.Font("techno_hideo.ttf", 90)
        smallText = pygame.font.Font("techno_hideo.ttf", 30)
        
        ###BUTTONS###
        
        #QUIT BUTTON
        if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 600 + 40 > mouse[1] > 600: #If the mouse is over the button, display a lighter version   
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 600, 500, 60))
            pygame.draw.rect(screen, white, (screenwidth/2 - 240, 610, 480, 40))
            if click[0] == 1: #If they click the quit button, quit
                pygame.quit()
        else:
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 600, 500, 60))
            pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 610, 480, 40))

        if screenwidth/2 + 250 > mouse[0] > screenwidth/2 - 250 and 530 + 40 > mouse[1] > 530: #If the mouse is over the button, display a lighter version
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 530, 500, 60))
            pygame.draw.rect(screen, white, (screenwidth/2 - 240, 540, 480, 40))
            if click[0] == 1: #If they click the play again button, restart the game loop
                gameLoop()
        else:
            pygame.draw.rect(screen, black, (screenwidth/2 - 250, 530, 500, 60))
            pygame.draw.rect(screen, darkgrey, (screenwidth/2 - 240, 540, 480, 40))

        #Play again text
        textSurf, textRect = text_objects("Play Again", smallText)
        textRect.center = ((screenwidth/2), (540 + 20))
        screen.blit(textSurf, textRect)

        #Quit text
        textSurf, textRect = text_objects("Quit", smallText)
        textRect.center = ((screenwidth/2), (610 + 20))
        screen.blit(textSurf, textRect)

        #You won Text
        textSurf, textRect = text_objects("You Won!", medText)
        textRect.center = ((screenwidth / 2), (screenheight * 0.25))
        screen.blit(textSurf, textRect)
        textSurf, textRect = text_objects("Congratulations!", medText)
        textRect.center = ((screenwidth / 2), (screenheight * 0.35))
        screen.blit(textSurf, textRect)

        #Score display text
        losingMessage = "Score:  " + str(player.score * 100 + player.lives * 100)
        textSurf, textRect = text_objects(losingMessage, mediumText)
        textRect.center = ((screenwidth / 2), (screenheight * 0.5))
        screen.blit(textSurf, textRect)
        
        pygame.display.update() #Update display
        clock.tick(30) #FPS to 30
 
#Create an 1152 by 832 sized screen (works with dimensions for tile map)
screenwidth = 1152
screenheight = 832
screen = pygame.display.set_mode((screenwidth, screenheight), 0, 32)
 
# Set the caption of the window
pygame.display.set_caption("Nick's Bricks!")
 
#Creates the sprites out of the classes
ball = Ball()
player = Player()
Hborder = hBorder()
VBorderr = VBorder_R()
VBorderl = VBorder_L()

#Creates the groups
balls = pygame.sprite.Group()
Hwalls = pygame.sprite.Group()
Vwalls = pygame.sprite.Group()
movingsprites = pygame.sprite.Group()
movingsprites.add(player)

#Adds the sprites to the groups
movingsprites.add(ball)
Hwalls.add(Hborder)
Vwalls.add(VBorderr)
Vwalls.add(VBorderl)
balls.add(ball)

clock = pygame.time.Clock() #Initialize clock

#######################################################################################################GAMELOOP###############################################################################################
def gameLoop():
    
    pygame.mixer.music.play(-1) #Play the background music

    #Set lives and score to starting values
    player.lives = 3
    player.score = 0
    
    #Reset the ball and player
    ball.reset()
    player.playerReset()

    #Tilemap for the level
    level = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,2,2,2,0,0,0],
        [0,0,2,2,2,2,2,0,0],
        [0,1,2,2,2,2,2,1,0],
        [0,0,2,2,2,2,2,0,0],
        [0,0,0,2,2,2,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]

    #Lists to store positions of metal bricks and bricks 
    MB_positions = []
    B_positions = []

    #Creates a group for metalbricks and bricks
    metalBricks = pygame.sprite.Group()
    bricks = pygame.sprite.Group()

    #Adds the positions of the bricks and metal bricks based on spot on tilemap
    for y in range(0, len(level)):
        for x in range(0,len(level[y])):
            if level[y][x]==1:
                MB_positions.append((x*128, y*64))
            if level[y][x]==2:
                B_positions.append((x*128, y*64))

    #For each position in the metal brick position list
    for position in MB_positions:
        #Create a metalbrick sprite, add it to the group, and display it at the position
        metalBrick = MetalBrick()
        metalBrick.display(position)
        metalBricks.add(metalBrick)

    #For each position in the brick position list
    for position in B_positions:
        #Create a metalbrick sprite, add it to the group, and display it at the position
        brick = Brick()
        brick.display(position)
        bricks.add(brick)
    
    done = False

    #Actual loop
    while not done:
        
        #If quit, quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(grey) #Fill the screen with the background colour

        #DRAW SCORE AND LIVES BOXES AND PUT TEXT INTO THEM
        pygame.draw.rect(screen, black, (65, 790, 170, 60))
        pygame.draw.rect(screen, darkgrey, (75, 800, 150, 50))

        pygame.draw.rect(screen, black, (887, 790, 227, 60))
        pygame.draw.rect(screen, darkgrey, (897, 800, 207, 50))

        text = pygame.font.Font("techno_hideo.ttf", 30)
        livesDisplay = "Lives: " + str(player.lives)
        textSurf, textRect = text_objects(livesDisplay, text)
        textRect.center = ((150), (815))
        screen.blit(textSurf, textRect)
        
        text = pygame.font.Font("techno_hideo.ttf", 30)
        scoreDisplay = "Score: " + str(player.score * 100)
        textSurf, textRect = text_objects(scoreDisplay, text)
        textRect.center = ((1000), (815))
        screen.blit(textSurf, textRect)
        
        #Check win condition
        if player.score == 21: #If they won, take them to the win screen
            gameWin()

        #Update the groups
        player.update()
        balls.update()
        Vwalls.update()
        Hwalls.update()
        metalBricks.update()
        bricks.update()

        #Collisions
        collisionBall_Hwalls = pygame.sprite.spritecollide(ball, Hwalls, False)
        collisionBall_Vwalls = pygame.sprite.spritecollide(ball, Vwalls, False)
        collisionPlayer_ball = pygame.sprite.spritecollide(player, balls, False)
        collisionBall_MetalBrick = pygame.sprite.spritecollide(ball, metalBricks, False)
        collisionBall_Brick = pygame.sprite.spritecollide(ball, bricks, True)

        #Collision action between ball and top wall
        for collision in collisionBall_Hwalls:
            #Invert y speed and play collision sound
            ball.speedy *= -1 
            pygame.mixer.Sound.play(collision_sound) 

        #Collision action between ball and side walls
        for collision in collisionBall_Vwalls:
            #Invert x speed and play collision sound
            ball.speedx *= -1
            pygame.mixer.Sound.play(collision_sound)

        #Collision action between ball and platform
        for collision in collisionPlayer_ball:
            if ball.rect.y <= collision.rect.top:
                #Invert y speed and play collision sound
                ball.speedy *= -1
                pygame.mixer.Sound.play(collision_sound)

        #Collision action between ball and metal brick
        for collision in collisionBall_MetalBrick:
            if ball.rect.centerx <= collision.rect.x or ball.rect.centerx >= collision.rect.x + 128: #If the ball collided on the vertical sides
                #Invert x speed and play collision sound
                ball.speedx *= -1
                pygame.mixer.Sound.play(collision_sound)
            elif ball.rect.centery <= collision.rect.y or ball.rect.centery >= collision.rect.y + 64: #If the ball collided on the horizontal sides
                #Invert y speed and play collision sound
                ball.speedy *= -1
                pygame.mixer.Sound.play(collision_sound)

         #Collision action between ball and brick
        for collision in collisionBall_Brick:
            if ball.rect.centerx <= collision.rect.left or ball.rect.centerx >= collision.rect.right: #If the ball collided on the vertical sides
                #Invert x speed and play collision sound, and add 1 to score
                ball.speedx *= -1
                player.score += 1
                pygame.mixer.Sound.play(collision_sound)
            elif ball.rect.centery <= collision.rect.top or ball.rect.centery >= collision.rect.bottom: #If the ball collided on the horizontal sides
                #Invert y speed and play collision sound, and add 1 to score
                ball.speedy *= -1
                player.score += 1
                pygame.mixer.Sound.play(collision_sound)

        #Moves the platform if the user presses the arrow keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-10, 0)
        if key[pygame.K_RIGHT]:
            player.move(10, 0)
        
        #Draw Everything
        movingsprites.draw(screen)
        Hwalls.draw(screen)
        Vwalls.draw(screen)
        metalBricks.draw(screen)
        bricks.draw(screen)

     
        #Update the screen
        pygame.display.flip()
         
        clock.tick(30) #Set FPS to 30

gameIntro() #Call the Game intro function
gameLoop()#When that is over, call the gameloop function
pygame.quit() #Finally, pygame.quit()
