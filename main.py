""" Author: Anson Tran

    Date:
    
    Description: This game is a 1v1 duel arena, for 2 players. Players will use 
                 two different keyboard layouts on the keyboard. Player 1 will
                 use WASD keys for movement, and letters G,H,J for commands. 
                 Player 2 will use the arrow keys for movement and comma,period,
                 slash for commands. The winner will be the player who kills 
                 their opponent first. Players can attack, block, and jump 
                 around on platforms.
"""

# I - IMPORT AND INITIALIZE
import asyncio
import pygame, sprites

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((920, 520)) 

# Global variable of what the game is doing
STATE = "intro"

def intro():
    '''This function displays the intro screen'''
    # Any reference to STATE refers to the global variable
    global STATE
    
    # D - DISPLAY
    pygame.display.set_caption("Welcome!")
    
    # E - ENTITIES
    background = pygame.image.load("rez/background.png")
    screen.blit(background, (0,0))
    
    # Background Music
    pygame.mixer.music.load("music/background/intro.ogg")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
    # Sprites
    title = sprites.Label(460,50,75,"Hellbound","center")
    play = sprites.Label(460,350,40,"play","center")
    instructions = sprites.Label(460,400,40,"instructions","center")
    pointer = sprites.Point()
    
    allSprites = pygame.sprite.OrderedUpdates(play,instructions,title,pointer)
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
 
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(60)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            # Quits the game
            if event.type == pygame.QUIT:
                STATE = "quit"
                keepGoing = False
                
            # Changes STATE if player clicks on the text
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Moves to game() if player clicks play
                if pointer.rect.colliderect(play.rect):
                    STATE = "play"
                    keepGoing = False
                    
                # Moves to instructions() if player clicks instructions
                if pointer.rect.colliderect(instructions.rect):
                    STATE = "instructions"
                    keepGoing = False
                
        # Sets the position of the pointer
        pointer.set_pos(pygame.mouse.get_pos())

        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
         
def instructions():
    '''This function displays the instructions screen'''
    
    # Any reference to STATE will refer to the global variable
    global STATE
    
    # D - DISPLAY
    pygame.display.set_caption("Help")
    
    # E - ENTITIES
    background = pygame.image.load("rez/background.png")
    screen.blit(background, (0,0))
    
    # Sprites
    title = sprites.Label(460,30,40,"Help","center")
    subtitle1 = sprites.Label(200,60,30,"Player 1 Controls","center")
    subtitle2 = sprites.Label(720,60,30,"Player 2 Controls","center")
    back = sprites.Label(460,450,30,"Return","center")
    
    text1 = ("Player 1 uses", "W         Jump", "A         Left", "S         Crouch", "D         Right", "G         Sword Attack", "H         Fireball", "J         Defend")
    text2 = ("Player 2 uses", "UP        Jump", "LEFT      Left", "DOWN      Crouch", "RIGHT     Right", "COMMA     Sword Attack", "PERIOD     Fireball", "SLASH     Defend")
    paragraph1 = []
    paragraph2 = []
    
    for line in range(len(text1)):
        paragraph1.append(sprites.Label(63,30*line + 100,20,text1[line],"left"))
        paragraph2.append(sprites.Label(583,30*line + 100,20,text2[line],"left"))
        
    text = pygame.sprite.Group(title,subtitle1,subtitle2,paragraph1,paragraph2)
    
    pointer = sprites.Point()
    
    allSprites = pygame.sprite.Group(pointer,text,back)
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
 
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(60)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            # Quits the game
            if event.type == pygame.QUIT:
                STATE = "quit"
                return False
            
            # Returns to intro() if user clicks on "return"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pointer.rect.colliderect(back.rect):
                    STATE = "intro"
                    keepGoing = False
                
        # Sets the position of the pointer
        pointer.set_pos(pygame.mouse.get_pos())
            
        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

def game():
    '''This function defines the game loop.'''
      
    global STATE
    
    # D - DISPLAY
    pygame.display.set_caption("Fight!")
    
    # E - ENTITIES
    background = pygame.image.load("rez/background.png")
    screen.blit(background, (0, 0))
    
    # Background Music
    pygame.mixer.music.load("music/background/game.ogg")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
    # Sound Effects
    block = pygame.mixer.Sound("music/fx/block.wav")
    block.set_volume(0.5)
    cut = pygame.mixer.Sound("music/fx/cut.wav")
    cut.set_volume(0.5)
    fireball = pygame.mixer.Sound("music/fx/fireball.wav")
    fireball.set_volume(0.5)

    # Sprites    
    
    # Construct Level
    platform = []
    x=0
    y=0
    # Reads from a text document
    for text in open("level.txt","r"):
        for digit in text:
            # If it is a 1, set a 30 by 1 platform
            if str(digit) == str(1):
                platform.append(sprites.Platform(x,y))
            x += 30
        y += 30
        x = 0
        
    health1 = sprites.HealthBar(screen,(screen.get_width()/5)*2,30,"right")
    health2 = sprites.HealthBar(screen,(screen.get_width()/5)*3,30,"left")
                
    
    level = pygame.sprite.Group(platform)
    
    player1 = sprites.Player(screen,"1",screen.get_width()/5,0,"right",level)
    player2 = sprites.Player(screen,"2",screen.get_width()/5*4,0,"left",level)
    
    endMessage1 = sprites.Label(460,230,60,"Player 1 Wins!","center")
    endMessage2 = sprites.Label(460,230,60,"Player 2 Wins!","center")
    
    players = pygame.sprite.Group(player1,player2)
    proj1 = pygame.sprite.Group()
    proj2 = pygame.sprite.Group()
    allSprites = pygame.sprite.OrderedUpdates(player1,player2,level,health1,health2)
    
    
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    delay = 0
 
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(60)
     
        # EVENT HANDLING
        for event in pygame.event.get():
            # Quits the game
            if event.type == pygame.QUIT:
                STATE = "quit"
                keepGoing = False
        
        pressed = pygame.key.get_pressed()
        
        # Do if healthbar 1 is not empty
        if not health1.dead():
            # Moves the player left
            if pressed[pygame.K_a]:
                player1.move(-6,"left")
                player1.state("movement")
            # Changes to crouch position
            elif pressed[pygame.K_s]:
                player1.state("crouch")
            # Moves the player right
            elif pressed[pygame.K_d]:
                player1.move(6,"right")
                player1.state("movement")
                
            # Attack/Defend
            else:
                # Sword attack
                if pressed[pygame.K_g]:
                    player1.state("attack")
                    if player1.sound():
                        cut.play()
                # Shoots a fireball if there isn't one on the screen
                elif pressed[pygame.K_h]:
                    if len(proj1.sprites()) == 0: 
                        projectile = sprites.Projectile(screen,player1.get_projData())
                        allSprites.add(projectile)
                        proj1.add(projectile)
                        fireball.play()
                    else:
                        player1.state("movement")
                        player1.stop("x")
                # Defending
                elif pressed[pygame.K_j]:
                    player1.state("defend")
                    if player1.sound():
                        block.play()
                # Otherwise, movement
                else:
                    player1.stop("x")
                    player1.state("movement")
                
            # Jumping
            if pressed[pygame.K_w]:
                player1.jump()
                
        # Tells the player to die if healthbar1 is empty
        else:
            player1.dead(True)
            
        # Do if healthbar 2 is not empty
        if not health2.dead():
            # Moves the player left
            if pressed[pygame.K_LEFT]:
                player2.move(-6,"left")
                player2.state("movement")
            # Changes to crouch position
            elif pressed[pygame.K_DOWN]:
                player2.state("crouch")
            # Moves the player right
            elif pressed[pygame.K_RIGHT]:
                player2.move(6,"right")
                player2.state("movement")
                
            # Attacking/Defending
            else:
                # Sword attack
                if pressed[pygame.K_COMMA]:
                    player2.state("attack")
                    if player2.sound():
                        cut.play()
                # Shoots a fireball if there isn't one on the screen
                elif pressed[pygame.K_PERIOD]:
                    if len(proj2.sprites()) == 0: 
                        projectile = sprites.Projectile(screen,player2.get_projData())
                        allSprites.add(projectile)
                        proj2.add(projectile)
                        fireball.play()
                    else: 
                        player2.state("movement")
                        player2.stop("x")
                # Defending
                elif pressed[pygame.K_SLASH]:
                    player2.state("defend")
                    if player2.sound():
                        block.play()
                # Otherwise Movement
                else:
                    player2.stop("x")
                    player2.state("movement")
            # Jumping
            if pressed[pygame.K_UP]:
                player2.jump()
        # Tells the player to die if healthbar 2 is empty
        else:
            player2.dead(True)
            
        # COLLISION DETECTION
        if player1.rect.colliderect(player2.rect):
            # If player 1 is attacking
            if player1.damage():
                # Reduced damage if player 2 is defending
                if player2.defend():
                    health2.loseHealth(2)
                # Full damage if player 2 is not
                else:
                    health2.loseHealth(10)
            # If player 2 is attacking
            if player2.damage():
                # Reduced damage if player 1 is defending
                if player1.defend():
                    health1.loseHealth(2)
                # Full damage if player 1 is not
                else:
                    health1.loseHealth(10)
            
        # Fireball collisions only do damage if the enemy is not defending, and will only affect your enemy
        if pygame.sprite.spritecollide(player1, proj2, False) and not player1.defend():
            health1.loseHealth(2)
            
        if pygame.sprite.spritecollide(player2, proj1, False) and not player2.defend():
            health2.loseHealth(2)
            
        # Displays a message of who wins, and starts 5 second delay
        if health1.dead():
            if endMessage2.alive() == False:
                allSprites.add(endMessage2)
            delay += 1
        if health2.dead():
            if endMessage1.alive() == False:
                allSprites.add(endMessage1)
            delay += 1
        
        # Sets back to intro once 5 second delay is over
        if delay == 300:
            STATE = "intro"
            keepGoing = False
            
        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
        
     
# Call the main function
async def main():
    '''This function defines the mainline logic for our game.'''
    playing = True
    # Calls the other functions depending on what state the game is in.
    while playing:
        if STATE == "intro":
            intro()
        if STATE == "instructions":
            instructions()
        if STATE == "play":
            game()
        if STATE == "quit":
            playing = False

        await asyncio.sleep(0)
            
    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
