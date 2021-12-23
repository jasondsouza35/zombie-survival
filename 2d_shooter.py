import pygame
import time
import random
import time
pygame.init() #Initializes the pygame

screenWidth = 1024 #Pixel meaurements for the program's window width and length
screenLength = 462
 
win = pygame.display.set_mode((screenWidth, screenLength)) #pygame.display.set_mode function sets the size of the pygame window, the dimennsions 1024 pixels by 462 pixels matches the typical full screen of a monitor
#win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #Option for fullscreen if desired
 
pygame.display.set_caption("Claymore: A Thousand Tales") #pygame.display.set_caption function sets the displayed window caption when the game is running

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')] #pygame.image.load function calls upon specific images from the shared folder based on the input from the user arrow keys
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('Background.png') #Functions calls and displays image for game background
char = pygame.image.load('standing.png') #Function calls and displays the idle image for the user's character

clock = pygame.time.Clock() #pygame.time.clock function defines the 'clock' to be used for other functions  






class player(object): #Creates a 'player' class, an object in the game
    def __init__(self,x,y,width,height): #Defines function which initializes 'player'
        self.x = x #No set value so that it can change dynamically when the player moves on the x axis 
        self.y = y #No set value so that it can change dynamically when the player moves on the y axis
        self.width = width #No set value, but usually set to the dimensions of the image of the player in this case 64
        self.height = height #No set value, but usually set to the dimensions of the image of the player, in this case 64
        self.vel = 5 #Sets velocity/speed of the player
        self.isJump = False #This will be used later to allow the player to jump 
        self.left = False #This will be used later to allow the player to move left
        self.right = False #This will be used later to allow the player to move right 
        self.walkCount = 0 #This will be used later to determine the position which the player is facing
        self.jumpCount = 10 #This will be used to set a cap for how long and high the player can jump
        self.standing = True #This will be used to assist in determing the position and  direction the player is facing
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #Sets the 'hitbox' for the player

    def draw(self, win): #Defines 'draw' function, used to display the characters on the screen
        if self.walkCount + 1 >= 27:
            self.walkCount = 0 #Determines the way the character is facing 

        if not(self.standing):
            if self.left: 
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y)) #Displays the image of when the character is facing left 
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y)) #Displays the image of when the character is facing right 
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y)) #Displays the image of when the character is facing right 
            else:
                win.blit(walkLeft[0], (self.x, self.y)) #Displays the image of when the character is facing left 
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self): #Function which is used when the player dies or collides with the enemies
        self.isJump = False #Player is spawned not jumping
        self.jumpCount = 10 #Sets a cap for how long and high the player can jump
        self.x = 400 #Sets respawn coordinates for x axis 
        self.y = 240 #Set respawn coordinates for y axis 
        self.walkCount = 0 #Determines the way the character is facing 

class projectile(object): #Creates a 'projectile' class, an object in the game
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = 255, 0, 0 #Sets the color of the projectile 
        self.facing = facing
        self.vel = 8 * facing #Sets how fast the projectile can travel 

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius) #Sets the shape of the projectile, in this instance it is a circle


class enemy(object): #Creates a 'enemy' class, an object in the game
    #Following lines call upon the images from the shared folder to be used for animations when walking in each direction
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x #No set value so that it can change dynamically when the enemy moves on the x axis
        self.y = y #No set value so that it can change dynamically when the enemy moves on the y axis
        self.width = width #No set value, but usually set to the dimensions of the image of the enemy in this instance 64
        self.height = height #No set value, but usually set to the dimensions of the image of the enemy, in this case 64
        self.end = end #No set value so that it can change dynamically, determines the distance of which how far the enemy can travel before turning back 
        self.path = [self.x, self.end] #The enemy will travel from it's default x coordinate to the end point before turning back 
        self.walkCount = 0 
        self.vel = 5 #How fast the enemy will travel
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) #The hitbox of the enemy
        self.health = 1 #Sets the health of the enemy to 1, meaning it will take two projectiles to kill the target
        self.visible = True #Will display the enemy on screen when the value is set to true 

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0 #Determines the way the character is facing

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y)) #Displays the image of when the enemy is facing right 
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y)) #Displays the image of when the enemy is facing left 
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #Creates a red rectangle above the enemy to represent their healthbar
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (25 * (1 - self.health)), 10)) #Creates a green rectangle above the enemy to represent the health, which will be taken away in chunks each projectile according to their health
            self.hitbox = (self.x + 17, self.y + 2, 31, 57) #Moves hitbox/healthbar along with the character sprite
            

    def move(self): #Makes it so that the enemy will move on its own 
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        global score #Global function calls upon the 'score' variable from outside the loop
        if self.health > 0: #If statement continues if the enemy still has more health
            self.health -= 1 #Subtracts one health from the enemy if it is shot
        else:
            enemies.pop(enemies.index(goblin)) #Function removes the enemy from the list, including the hitbox and its sprite once it has less than 0 health
            score += 1 #Adds 1 to the 'score' variable everytime an enemy is killed



class bigenemy(object):
    #Following lines call upon the images from the shared folder to be used for animations when walking in the corresponding direction
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 2.7
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 14 #Makes the goblin take 15 bullets before dying
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (3.333 * (14 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        global score
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False 
            enemies.pop(enemies.index(goblin)) 
            score += 1 

            
class flyenemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x 
        self.y = y  
        self.width = width  
        self.height = height 
        self.end = end 
        self.path = [self.x, self.end]  
        self.walkCount = 0
        self.vel = 7 
        self.hitbox = (self.x + 17, self.y + 2, 31, 57) 
        self.health = 0 
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0 

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y)) 
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y)) 
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #Creates a red rectangle above the enemy to represent their healthbar
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (50 * (0 - self.health)), 10)) #Creates a green rectangle above the enemy to represent the health, which will be taken away in chunks each projectile according to their health
            self.hitbox = (self.x + 17, self.y + 2, 31, 57) #Moves hitbox/healthbar along with the character sprite
            pygame.draw.rect(win, (0,150,150), self.hitbox,2) #Draws the hitbox of the enemy 

    def move(self): #Makes it so that the enemy will move on its own 
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        global score 
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False #Removes the enemy from the screen 
            enemies.pop(enemies.index(goblin)) #Removes the enemy from the list of enemies 
            score += 1 #Adds 1 score for every enemy you kill 
        

def redrawGameWindow():
    win.blit(bg, (0,0)) #Refills the background image to its original state once something has something has walked over the affected area 
    text = font.render('Score: ' + str(score), 1, (255,0,0)) #Prints the score of the user 
    win.blit(text, (485, 150)) #Draws the text on the screen
    man.draw(win) #Draws the main character on the screen 
    for bullet in bullets: #For every bullet in the bullet list
        bullet.draw(win) #Draws the bullet 
    for goblin in enemies: #For every bullet in the bullet list
        goblin.draw(win) #Draws the bullet 
    pygame.display.update() #Updates the screen to ensure player gets the most updated image of the game 

def gameover():
    global run #Global function calls upon the 'run' variable from outside the loop
    music = pygame.mixer.music.pause() #Function stops the game music
    EndMusic = pygame.mixer.music.load('BossTheme.mp3') #pygame.mixer.music.load calls and loads a MP3 track from its shared folder into the program 
    EndMusic = pygame.mixer.music.play(-1) #pygame.mixer.music.load plays loaded music in the game
    pygame.draw.rect(win, (0,0,0), (0, 0, screenWidth, screenLength)) #Black background rectangle
    pygame.draw.rect(win, (0,230,0), (100, 275, 300, 150)) #Green rectangle     
    pygame.draw.rect(win, (230,0,0), (618, 275, 300, 150)) #Red rectangle
    font2 = pygame.font.SysFont('comicsans', 50, True) #Large font
    font3 = pygame.font.SysFont('comicsans', 40, True) #Slightly smaller font
    gameover = font2.render('Game Over', 1, (255,255,255)) #Renders white text onto the screen
    playagain = font3.render('Would you like to play again?', 1, (255, 255, 255))
    yes = font2.render('Yes', 1, (255,255,255))
    no = font2.render('No', 1, (255,255,255))
    win.blit(gameover, (405, 100)) #Prints 'Game Over'
    win.blit(playagain, (290, 150)) #Prints on the window asking the user if they would like to play again
    win.blit(yes,  (210,335)) #Prints yes in the green box
    win.blit(no,  (740,335)) #Prints no in the red box
    pygame.display.update() #Updates the display to show the text/rectangles/colours
    while run == False: #Continues if 'run' variable is false
        for event in pygame.event.get(): #Function checks for any events in the program
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #If statement continues if the event from the user is a left mouse click
                x, y = pygame.mouse.get_pos() #Gets the x and y position of the mouse click
                if x > 100 and x < 400 and y > 275 and y < 425: #If statement continues if the mouse click is within the green rectangle coordinates
                        run = True #'run' variable becomes true, therefore, the while loop the function is in can loop again
                        EndMusic = pygame.mixer.music.stop() #Function stops playing the end screen music
                elif x > 618 and x < 918 and y > 275 and y < 425: #If statement continues if the mouse click is within the red rectangle coordinates    
                        pygame.quit() #Quit function closes and quits the game
                        quit() #Asks the user if they would like to close IDLE 
                




run = True #Defines the 'run' variable as True

#Main Game Loop

while run: #While loop keeps running until 'run' is no longer True
    font = pygame.font.SysFont('comicsans', 30, True) #Function defines text and its size
    enemies = [] #Defines the 'enemies' list everytime the game is started, removing all enemies from the screen at the start of every new game
    bullets = [] #Defines the 'bullets' list everytime the game is started, removing all bullets from the screen at the start of every new game
    score = 0 #Defines the 'score' variable to 0 everytime the game is started
    man = player(400, 240, 64,64) #Sets coordinates for the player to be at for the begining of each game
    SpawnPointX = random.randint(0,50) #Sets spawn point coordinates for the enemies
    reload = time.time() #Creates the 'reload' variable using the time.time function as a timer throughout the program
    pygame.time.set_timer(pygame.USEREVENT, random.randrange(3000, 7000)) #Time.set_timer function sets a timer in milliseconds to determine the amount of time for a loop to be repeated again, the randrange function uses a random integer from the provided range for the timer
    pygame.time.set_timer(pygame.USEREVENT + 1, random.randrange(7000, 14000))
    pygame.time.set_timer(pygame.USEREVENT + 2, random.randrange(4000, 11000))
    music = pygame.mixer.music.load('Guile.mp3') #Loads 'Guile' song from shared folder
    music = pygame.mixer.music.play(-1) #Plays 'Guile'

    
    while run: #While loop keeps running until 'run' is no longer True
        clock.tick(27)  #Sets the speed/pace of the program
        
        for goblin in enemies:
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                    run = False #If the player collides with the enemy the game will end 
                        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #If you click the 'X' at the top right corner it will close the game 
            if event.type == pygame.USEREVENT: #Will randomly add enemies to the enemy list 
                enemies.append(enemy(SpawnPointX, 240, 64, 64, 990))
            if event.type == pygame.USEREVENT + 1: #Will randomly add enemies to the enemy list 
                enemies.append(bigenemy(SpawnPointX, 240, 64, 64, 990))
            if event.type == pygame.USEREVENT + 2: #Will randomly add enemies to the enemy list 
                SpawnPointY = random.randint(55,75) #Creates a random spawn point on the Y axis 
                enemies.append(flyenemy(SpawnPointX, SpawnPointY, 64, 64, 1000))
                
        for bullet in bullets: #Sets 'bullet' from 'bullets' list
            for goblin in enemies: #Sets 'goblin' from 'enemies' list
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                        goblin.hit() #Runs the 'hit' function, deciding to either lower the goblin's health or remove it when it is hit with a projectile
                        bullets.pop(bullets.index(bullet)) #If a bullet collides with an enemy, it is removed from the screen, including it's visual appearence, hitbox, and position in the 'bullets' list
                                          
                        
                    
            if bullet.x < 1024 and bullet.x > 0: #Parameters for the bullet distance across the user's screen 
                bullet.x += bullet.vel #Bullet velocity/distance once shot
            else:
                bullets.pop(bullets.index(bullet)) #Will remove the bullet from the game once it reaches a certain point on the 'X' axis 

        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_SPACE] and time.time() - reload >= 0.5: #If statement continues if the user holds space and there was a 0.5 second interval since the previous iteration of this if statement
            if len(bullets) < 5: #If statement continues if there are 5 or less bullets in the list
                if man.left:
                    facing = -1
                else:
                    facing = 1
                bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing)) #append function creates a list for all the bullets on the screen, preventing the user from loading more than 5 bullets on the screen at a time
            reload = time.time() #Resets the time.time function for the 'reload' variable so the counter restarts at 0 everytime the space bar is held down
            
            
        if keys[pygame.K_LEFT] and man.x > man.vel: #If statement continues if the user holds the left arrow key and the x.axis of the player does not exceed the game's boundries
            man.x -= man.vel #Subtracts from the 'X' axis due to the character moving left
            man.left = True #Moving left so it is true
            man.right = False #Not moving right so it is false 
            man.standing = False #No longer at a neutral position 
        elif keys[pygame.K_RIGHT] and man.x < 1024 - man.width - man.vel: #Determines boundries for the character, creating space where the user's character can move and where it cannot
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
            
        if not(man.isJump):
            if keys[pygame.K_UP]: 
                man.isJump = True #Man jumps if user holds up key
                man.right = False #Left/right arrow keys are considered false when jumping as a precautionary for error
                man.left = False
                man.walkCount = 0
            elif keys[pygame.K_UP]:
                man.y += man.vel #Adds to the y.axis of the character corresponding to the velocity 
                man.up = True
                man.down = False
        else:
            if man.jumpCount >= -10: #If statement continues if the player jumpcount is greater than or equal to negative 10
                neg = 1 #Will slowly decrease the jump count of the player to limit how long the player is airborne for
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg #Determines the speed of which the player will fall down, subtracts from the y.axis of the player
                man.jumpCount -= 1 #Once it reaches zero the player will no longer be airborne 
            else:
                man.isJump = False
                man.jumpCount = 10 #Once the player hits jump, their jumpcount will be set to 10 which will control how long the player can be airborne for 
                
        redrawGameWindow() #Runs the 'redrawGameWindow' at the end of every loop to refresh the game display

    gameover() #Runs the 'gameover' function if the conditions for the while loop are no longer met, giving an end menu for the player

