import pygame
class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for our player'''
    def __init__(self,screen,playerNum,startX,startY,facing,level):
        '''The initializer takes a screen surface, starting x and y value, and facing direction.
        It loads animation images, sets the rect attributes, etc.'''
        # Initializes the super class
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.__anims = {}
        
        self.__playerNum = playerNum
        
        # Loads images for the animations
        self.animsLoad("sprint",1)
        self.animsLoad("jump",8)
        self.animsLoad("crouch",2)
        self.animsLoad("defend",12)
        self.animsLoad("attack",8)
        self.animsLoad("dying",5)
        self.animsLoad("idle",4)
        
        
        # Initial Image  
        self.image = self.__anims ["jumpright0"]
        
        # Gets image rect and sets the starting position
        self.getRect(self.image)
        self.rect.top = startY
        self.rect.centerx = startX
        
        # Stats
        self.__facing = facing       # Direction player is facing
        self.__count = 0             # Continuous Counter
        self.__changeX = 0           # Change in x value
        self.__changeY = 0           # Change in y value
        self.__air = True            # Shows whether player is in the air or not
        self.__state = "movement"    # Shows the state the player is in
        self.__x = self.rect.centerx # The current x value
        self.__y = self.rect.bottom  # The current y value
        self.__list = []             # A list of collided objects
        self.__level = level         # A list of blocks that the player can collide with
        self.__animation = "jump"    # The animation currently being shown
        self.__damage = False        # Allows player to do damage if True
        self.__defend = False        # Negates damage done by other players if True
        self.__dead = False          # States whether the player is dead
        self.__sound = False         # Tells whether sound should be played
        
    def animsLoad(self,animation,num):
        '''Takes an animation type, and range to load images'''
        for image in range(num):
            
            # Adds image facing right to dictionary with key value (animation type + facing + number)
            self.__anims [animation + "right" + str(image)] = pygame.image.load("rez/character" + self.__playerNum + "/" + animation + str(image) + ".png")
            
            # Flips image above and adds to dictionary
            self.__anims [animation + "left" + str(image)] = pygame.transform.flip(self.__anims[str(animation) + "right" + str(image)], True, False)
        
    def anim(self,animation,facing,count,delay):
        '''Changes the image, resets the rect, and repositions the player'''
        # Gets the current rect of the player
        self.holdRect(self.rect.centerx,self.rect.bottom)
        
        # Resets the counter if showing a new animation
        if self.__animation != animation:
            self.__count = 0
            
        # Sets the requested image
        self.image = self.__anims[str(animation) + str(facing) + str(int(self.counter(count,delay)))]
        
        # Gets the new rect attributes
        self.getRect(self.image)
        
        # Resets the player in the correct position
        self.setRect(self.__x,self.__y)
        
        # Sets value to current animation
        self.__animation = animation
        
    def counter(self,number,delay):
        '''Counter used in the anim method. number is the number of frames the animation lasts, not number of images'''
        # Resets the number if greater than # of images, else adds 1
        if self.__count >= number-1:
            self.__count = 0
        else:
            self.__count +=1
            
        # -1 is a sentinal value, which would go to the normal counter
        # Else, divide by the delay, which changes image every delayth frame
        if delay != -1:
            return self.__count/delay
        else:
            return self.__count
        
    def gravity(self):
        '''Adds gravity to the player'''
        # Gravity increases by 0.5 per frame
        self.__changeY += 0.5
                
    def setRect(self,x,y):
        '''Sets the rect of the player'''
        # -1 is a sentinal value, else sets the rect values of the player
        if x != -1:
            self.rect.centerx = x
        if y != -1:
            self.rect.bottom = y
            
    def move(self,dirXY,facing):
        '''Faces and moves the player in a direction'''
        self.__changeX = dirXY
        self.__facing = facing
        
    def stop(self,dirXY):
        '''Stops player from moving in the requested direction'''
        # Stops player from moving left or right
        if dirXY == "x":
            self.__changeX = 0
        
        # Stops player from moving up or down
        if dirXY == "y":
            self.__changeY = 0
        
    def jump(self):
        '''Lets the player jump if the player is on the ground'''
        # If player is on the ground, jump
        if self.__air == False:
            self.air(True)
            self.__changeY -= 10
    
    def air(self,state):
        '''Sets value to True/False depending on whether the player is in the air'''
        # Sets the state of the player
        self.__air = state
        
    def holdRect(self,x,y):
        '''Holds the current rect of the player'''
        # Sets the x and y to two instance variables
        self.__x = x
        self.__y = y
            
    def getRect(self,image):
        '''Gets the rect of the image'''
        # Returns the rect of the image
        self.rect = image.get_rect()
        
    def state(self,state):
        '''Sets the state of the player: "movement","attack","defend" '''
        # Sets state
        self.__state = state
        
    def damage(self):
        '''Tells us whether the player is taking damage'''
        # True if taking damage
        if self.__damage:
            return True
        # False if not
        else:
            return False
        
    def defend(self):
        '''Tells us whether the player is defending'''
        # True if defending
        if self.__defend:
            return True
        # False if not
        else:
            return False
        
    def get_projData(self):
        '''Gets data needed for projectile instances'''
        # Returns direction facing, left or right rect, centery, and player number
        if self.__facing == "right":
            return [self.rect.right,self.rect.centery,self.__facing,self.__playerNum]
        if self.__facing == "left":
            return [self.rect.left,self.rect.centery,self.__facing,self.__playerNum]
    
    def dead(self,state):
        '''Sets the player to be dead or not'''
        # True - Dead, False - Alive
        self.__dead = state
        
    def sound(self):
        '''Allows the sound to be played'''
        return self.__sound
        
    def update(self):
        '''A method that will be called automatically to reposition the
        player sprite on the screen.'''
        
        # Adds gravity to the player
        self.gravity()
        
        # A list of platforms the player collides with
        self.__list = pygame.sprite.spritecollide(self,self.__level,False)

        # Stops gravity if player collides with platform and going down
        if self.__list and self.__changeY >= 0:
            self.setRect(-1,self.__list[0].rect.top)
            self.air(False)
            self.stop("y")
               
        # Moves the player left and right
        self.rect.x += self.__changeX
        
        # Moves the player up and down
        self.rect.y += self.__changeY
        
        # Stops the player if collides with left side of the screen
        if self.rect.left <= 0 and self.__changeX < 0 :
            self.rect.left = 0
            self.stop("x")
            self.state("movement")
            
        # Stops the player if collides with right side of the screen            
        if self.rect.right >= self.__screen.get_width() and self.__changeX > 0:
            self.rect.right = self.__screen.get_width()
            self.stop("x")
            self.state("movement")
            
        # Sets the animation to dying animation, if dead
        if self.__dead:
            self.stop("x")
            
            # Stops animation from repeating
            if self.__count < 99:
                # Dying animation, 100 frames, 20 frames per image
                self.anim("dying",self.__facing,100,20)
            
        # If alive, determine animation
        if not self.__dead:
            
            # If state is "attack"
            if self.__state == "attack":
                self.__defend = False
                
                # Only attack if on the ground
                if self.__air == False:
                    
                    # Attack animation, total of 32 frames, 4 frames per image
                    self.anim("attack",self.__facing,32,4)
                    self.stop("x")
                        
                    # Moves player forward if after 3rd image
                    if self.__count >= 12 and self.__count%4 >= 3:
                        # Allows player to damage other players
                        self.__damage = True
                        
                        # Allows cutting sound to play
                        self.__sound = True
                        
                        # Move player in direction the player is facing
                        if self.__facing == "left":
                            self.move(-25,"left")
                        elif self.__facing == "right":
                            self.move(25,"right")
                    
                    # Turns off damage
                    else:
                        self.__damage = False
                        self.__sound = False
                    
                # If in air, set state to "movement"
                else:
                    self.__damage = False
                    self.state("movement")
                    self.stop("x")
                    
            # If state is "defend"
            if self.__state == "defend":
                self.__damage = False
                
                # If player is stationary and on the ground
                if self.__air == False and self.__changeX == 0:
                    # Blocks damage
                    self.__defend = True
                    # Defend animation, 12 frames, no delay
                    self.anim("defend",self.__facing,12,-1)
                    self.stop("x")
                    if self.__count%2 == 0:
                        self.__sound = True
                    
                # Otherwise, set state to "movement"
                else:
                    self.__sound = False
                    self.state("movement")
                    self.stop("x")
                    self.__defend = False
            
            # If state is "crouch"
            if self.__state == "crouch":
                self.__damage = False
                self.__defend = False
                
                # If player is on the ground and not moving
                if self.__air == False and self.__changeX == 0:
                    # Crouch animation, 60 frames, 30 frames per image
                    self.anim("crouch",self.__facing,60,30)
                    
                # Otherwise, sets state to movement
                else:
                    self.state("movement")
                    self.stop("x")
    
            # If state is "movement"
            if self.__state == "movement":
                self.__damage = False
                self.__defend = False
                
                # If the player is on the ground and not moving
                if self.__air == False and self.__changeX == 0:
                    # Idle animation, 120 frames, 30 frames per image
                    self.anim("idle",self.__facing,120,30)
                    
                # If the player is on the ground and moving
                if self.__air == False and self.__changeX != 0:
                    # Sprint animation, 1 frame, no delay
                    self.anim("sprint",self.__facing,1,-1)
                    
                # If the player is in the air
                if self.__air == True:
                    # Jump animation, 8 frames, no delay
                    self.anim("jump",self.__facing,8,-1)
                    
class Platform(pygame.sprite.Sprite):
    '''This class defines the sprite for platforms'''
    def __init__(self,left,top):
        '''This initializer takes the screen, left, and top positions for the platform sprites'''
        
        # Initializes the super class
        pygame.sprite.Sprite.__init__(self)

        # Sets image
        self.image = pygame.image.load("rez/surface.png")
        
        # Sets rect
        self.rect = self.image.get_rect()
        
        # Sets position of the sprite
        self.rect.top = top
        self.rect.left = left
        
class HealthBar(pygame.sprite.Sprite):
    '''This class defines the sprite for healthbars'''
    def __init__(self,screen,x,y,align):
        '''The initializer takes the screen, x,y, and alignment'''
        
        # Initiate the super class
        pygame.sprite.Sprite.__init__(self)
        
        # Beginning health of 200
        self.__health = 200
        
        # Sets the image
        self.image = pygame.Surface((self.__health,10)).convert()
        self.image.fill((255,0,0))
        
        # Sets the rect
        self.rect = self.image.get_rect()
        self.rect.top = y
        
        # Stats
        self.__align = align # Side to align the sprite
        self.__x = x         # x value
        self.__y = y         # y value
        self.__dead = False  # Sets to True when player dies
        
        # Aligns the sprite left or right
        if self.__align == "right":
            self.rect.right = self.__x
        if self.__align == "left":
            self.rect.left = self.__x
        
    def loseHealth(self,damage):
        '''Takes away health'''
        # Subtracts damage from health
        self.__health -= damage
        
    def dead(self):
        '''Tells us if player is dead or alive'''
        if self.__dead:
            return True
        else:
            return False
        
    def update(self):
        '''A method that will be called automatically to set the health of the player'''
        # Reduces the healthbar if still alive
        if self.__health >= 1:
            self.image = pygame.Surface((self.__health,10)).convert()
            self.image.fill((255,0,0))
            self.rect = self.image.get_rect()
        
            if self.__align == "right":
                self.rect.right = self.__x
            if self.__align == "left":
                self.rect.left = self.__x
            self.rect.top = self.__y
            
        # Otherwise, kills the sprite and tells player that it is dead
        else:
            self.__dead = True
            self.__health = 0
            self.kill()
        
class Projectile(pygame.sprite.Sprite):
    '''This class defines the sprite for fireballs'''
    def __init__(self,screen,playerData):
        '''This initializer takes the screen, and a list of playerdata as attributes'''
        # Initializes the super class
        pygame.sprite.Sprite.__init__(self)
        
        # Player data is a list of values from the player sprite It contains:
        #     [self.rect.right,self.rect.centery,self.__facing,self.__playerNum]
        self.__screen = screen
        self.__x = playerData[0]
        self.__y = playerData[1]
        self.__direction = playerData[2]
        self.__num = playerData[3]
        self.__count = 0
        
        # The speed that the sprite accelerates by per frame
        self.__accelerate = 0.35
        
        # Loads images of the player facing left and right, and adds to a dictionary
        self.__projAnims = {}
        for image in range(6):
            self.__projAnims ["projright" + str(image)] = pygame.image.load("rez/projectile" + self.__num + "/projectile" + str(image) + ".png")
            self.__projAnims ["projleft" + str(image)] = pygame.transform.flip(self.__projAnims["projright" + str(image)],True,False)
        
        # Sets the initial image and rect values
        self.image = self.__projAnims["proj" + self.__direction + str(self.__count)]
        self.rect = self.image.get_rect()
        self.rect.x = self.__x
        self.rect.centery = self.__y
        
        # Gets the rect attributes to reset when changing images
        if self.__direction == "left":
            self.__resetX = self.rect.left
        if self.__direction == "right":
            self.__resetX = self.rect.right
            
    def update(self):
        '''A method that will be called automatically to reposition the
        fireball sprite on the screen.'''
        # Accelerates the fireball
        self.__accelerate += 0.35
        
        # Gets the current rect attributes
        if self.__direction == "left":
            self.__resetX = self.rect.left
        elif self.__direction == "right":
            self.__resetX = self.rect.right
            
            
        self.__count += 1
        # Once the fireball runs through all 5 images, resets to 3rd image
        if self.__count >= 50:
            self.__count = 30
            
        # Changes the image of the fireball
        self.image = self.__projAnims ["proj" + self.__direction + str(int(self.__count / 10))]
        
        self.rect = self.image.get_rect()
            
        # Resets the sprite's position and moves it in the player's direction
        if self.__direction == "left":
            self.rect.left = self.__resetX
            self.rect.x -= self.__accelerate
        if self.__direction == "right":
            self.rect.right = self.__resetX
            self.rect.x += self.__accelerate
        self.rect.centery = self.__y
        
        # Kills itself if goes out of the screen
        if self.rect.right >= self.__screen.get_width():
            self.kill()
        if self.rect.left <= 0:
            self.kill()
            
class Label(pygame.sprite.Sprite):
    '''This class defines the sprite for text in-game'''
    def __init__(self,x,y,size,message,align):
        '''This initializer takes the x,y,text size, message, and alignment'''
        # Initializes the super class
        pygame.sprite.Sprite.__init__(self)
        
        # Sets the font and values
        self.__font = pygame.font.Font("rez/ARCADECLASSIC.TTF", size)
    
        # Sets the image attributes
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        
        # Aligns the text
        if align == "center":
            self.rect.centerx = x
        if align == "left":
            self.rect.left = x
        if align == "right":
            self.rect.right = x
        self.rect.top = y
        
class Point(pygame.sprite.Sprite):
    '''This class defines the sprite for the mouse pointer'''
    def __init__(self):
        '''This initializer defines the image and rect for the mouse pointer sprite'''
        
        # Initializes the super class
        pygame.sprite.Sprite.__init__(self)
        
        # Loads the mouse image, sets image and rect values
        self.__point = pygame.image.load("rez/pointer.gif")
        self.image = self.__point
        self.rect = self.image.get_rect()
        
    def set_pos(self,coords):
        '''Sets the position of the mouse'''
        self.rect.center = coords
    
        
