# Name: game.py
# Author: Jason Nguyen
# Last Revision: 4/29/14
# Version 0.2

import pygame, glob, random, math

def error_message():
    print("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##################################################
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                      error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##################################################
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")

class Shooter(pygame.sprite.Sprite):
    """ Main guy that user controls """

    def __init__(self, screen_width, screen_height, health = 800):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/shooter_front.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.health = health
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x_move = 0
        self.y_move = 0
        self.frame_count = 0

    def get_health(self):
        return str(self.health)

    def update(self):
        if self.x_move != 0 and self.rect.x+self.x_move < self.screen_width\
           - self.image.get_width() and self.rect.x + self.x_move > 0:
            self.rect.x += self.x_move
            self.frame_count += 1
            
        if self.y_move != 0 and self.rect.y + self.y_move < self.screen_height\
           - self.image.get_height() and self.rect.y + self.y_move > 0:
            self.rect.y += self.y_move
            self.frame_count += 1

        if self.frame_count > 20:
            self.frame_count = 0
            self.image = pygame.transform.flip(self.image, True, False)

class PowerUp(pygame.sprite.Sprite):
    """ Represents the power up """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/1up.png")
        self.rect = self.image.get_rect()
        self.tick = 0
        self.image_num = 1

    def update(self):
        self.tick += 1

        if self.tick > 10 and self.image_num == 1:
            self.image = pygame.image.load("images/2up.png")
            self.image_num = 2
            self.tick = 0
        elif self.tick > 10 and self.image_num == 2:
            self.image = pygame.image.load("images/1up.png")
            self.image_num = 1
            self.tick = 0

    def effect(self):
        None

class PowerHealth(PowerUp):
    """ Power up health """
    def effect(self):
        shooter.health += 100

class PowerSpread(PowerUp):
    """ Spread Shot """
    def effect(self):
        None
class PowerBomb(PowerUp):
    """ A bomb that lays by player """
    def effect(self):
        bomb = Bomb()
        bomb.rect.x = shooter.rect.x
        bomb.rect.y = shooter.rect.y
        allgroup.add(bomb)

class Bomb(pygame.sprite.Sprite):
    """ A bomb that blows up """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.anis = glob.glob("images/bomb_*.png")
        self.on_image = 0
        self.anis.sort()
        self.image = pygame.image.load(self.anis[self.on_image])
        self.image.set_colorkey((255,255,255))
        self.tick = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.tick += 1
        if self.tick > 30:
            if self.on_image == 3:
                for i in range(1,10):
                    bullet = Bullet()
                    bullet.rect.x = self.rect.x
                    bullet.rect.y = self.rect.y
                    bullet.x_move = math.sin(i)*25
                    bullet.y_move = math.cos(i) *25
                    bullet.add(allgroup)
                    bullet.add(bullet_list)
                self.kill()
            else:
                self.on_image +=1
            self.image = pygame.image.load(self.anis[self.on_image])
            self.image.set_colorkey((255,255,255))
            self.tick = 0

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet """
    def __init__(self,fill = (255,0,0)):
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([6, 6])
        self.image.fill(fill)
        self.rect = self.image.get_rect()
        self.x_move = 5
        self.y_move = 5
 
    def update(self):
        """ Move the bullet. """
        self.rect.x += self.x_move
        self.rect.y += self.y_move

class Zombie(pygame.sprite.Sprite):
    """ Zombie that attacks shooter """
    
    def __init__(self, health = 10):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("images/zombie_front.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.health = health
        self.frame_count = 0

    def update(self):
        if self.rect.x < shooter.rect.x:
            self.rect.x += 1
            self.frame_count += 1
        else:
            self.rect.x -= 1
            self.frame_count += 1
        if self.rect.y < shooter.rect.y:
            self.rect.y += 1
            self.frame_count += 1
        else:
            self.rect.y -= 1
            self.frame_count += 1
            
        # flip image after a couple of frames
        if self.frame_count > 20:
            self.frame_count = 0
            self.image = pygame.transform.flip(self.image, True, False)

class HealthBar(pygame.sprite.Sprite):
    """ The healthbar that changes health """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((800,10))
        self.image.fill((255,51,51))
        self.rect = self.image.get_rect()

    def display(self):
        self.image = pygame.Surface((shooter.health,10))
        self.image.fill((255,51,51))
        screen.blit(self.image,(100,0))
    

# start pygame
pygame.init()
red = 255,51,51
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
done = False
score = 0
wave = 1
spawners = 1
wave_delay_max = 100
wave_delay = 0

# set background
background = pygame.image.load("images/background_1000x800.png").convert()
backgroundRect = background.get_rect()

# Make nuclear spawner
nuclear = pygame.image.load("images/nuclear.png").convert()
nuclear_rect = nuclear.get_rect()

# Make Sprites
shooter = Shooter(screen_width,screen_height)
shooter.rect.x = (screen_width/2) - (shooter.image.get_width()/2)
shooter.rect.y = (screen_height/2) - (shooter.image.get_height()/2)
zombie = Zombie()
zombie.rect.x = random.randint(0,nuclear_rect[0])
zombie.rect.y = random.randint(0,nuclear_rect[1])

# Make sprite groups
zombiegroup = pygame.sprite.Group()
allgroup = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# add sprites to groups
allgroup.add(shooter)
zombiegroup.add(zombie)
allgroup.add(zombie)

# create healthbar
healthbar = HealthBar()

# the text surfaces
deluxeFont = pygame.font.SysFont("DeluxeFont Regular", 10)

# main loop
while not done:
    
    # check if done and keyboard inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # If key is pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                shooter.y_move = -2
            if event.key == pygame.K_s:
                shooter.y_move = 2
            if event.key == pygame.K_d:
                shooter.x_move = 2
            if event.key == pygame.K_a:
                shooter.x_move = -2
            if event.key == pygame.K_1:
                pos = pygame.mouse.get_pos()
                print(allgroup)
            if event.key == pygame.K_2:
                bomb = Bomb()
                bomb.rect.x = 100
                bomb.rect.y = 100
                allgroup.add(bomb)
            if event.key == pygame.K_3:
                powerup.effect()
                
                
                
        # If key is lifted up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                shooter.y_move = 0
            if event.key == pygame.K_s:
                shooter.y_move = 0
            if event.key == pygame.K_d:
                shooter.x_move = 0
            if event.key == pygame.K_a:
                shooter.x_move = 0
                
        # Fire a bullet
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet()
            pos = pygame.mouse.get_pos()
            # Set the bullet so it is where the shooter is
            halfofshooter = shooter.rect.x + 50
            if halfofshooter > pos[0]:
                bullet.rect.x = shooter.rect.x
            else:
                bullet.rect.x = shooter.rect.x + 95
                
            bullet.rect.y = shooter.rect.y +50

            # from shooter point to mouse point, calculate angle and
            # set dx and dy
            rise = bullet.rect.x - pos[0]
            run = bullet.rect.y - pos[1]
            try:
                angle = math.atan(rise/run)
            except:
                angle = 1

            if pos[1] < bullet.rect.y:
                bullet.x_move = math.sin(angle) * -20
                bullet.y_move = math.cos(angle) * -20
            else:
                bullet.x_move = math.sin(angle) * 20
                bullet.y_move = math.cos(angle) * 20
            
            # Add the bullet to the lists
            allgroup.add(bullet)
            bullet_list.add(bullet)


    # check if shooter is hit by zombie
    shooter_hit = pygame.sprite.spritecollide(shooter, zombiegroup, False)
    for hit in shooter_hit:
        shooter.health -=1

    powerup_get = pygame.sprite.spritecollide(shooter, powerup_group, True)
    for powerup in powerup_get:
        shooter.health += 100
    

    # check if bullet hits zombies
    for bullet in bullet_list:
        bullet_hit = pygame.sprite.spritecollide(bullet, zombiegroup, True)

        #add power up
        #if bullet_hit:
         #   powerup = PowerUp()
          #  powerup.rect.x = 300
           # powerup.rect.y = 400
            #allgroup.add(powerup)
            #powerup_group.add(powerup)
                                              
                                              

        for zombie in bullet_hit:
            bullet_list.remove(bullet)
            allgroup.remove(bullet)
            score += 1
        
        if bullet.rect.x > (screen_width+10) or bullet.rect.x < -10\
           or bullet.rect.y >\
           (screen_height+10) or bullet.rect.y < -10:
            bullet_list.remove(bullet)
            allgroup.remove(bullet)

    allgroup.update()

    clock.tick(60)
    
    screen.blit(background, backgroundRect)


    # spawn more spawners
    if spawners == 1:
        screen.blit(nuclear, (0,0))
    elif spawners == 2:
        screen.blit(nuclear, (0,0))
        screen.blit(nuclear, ((screen_width - nuclear_rect[2]),
                              (screen_height - nuclear_rect[3])))
    elif spawners == 3:
        screen.blit(nuclear, (0,0))
        screen.blit(nuclear, ((screen_width - nuclear_rect[2]),
                              (screen_height - nuclear_rect[3])))
        screen.blit(nuclear, ((screen_width - nuclear_rect[2]),0))
    else:
        screen.blit(nuclear, (0,0))
        screen.blit(nuclear, ((screen_width - nuclear_rect[2]),
                              (screen_height - nuclear_rect[3])))
        screen.blit(nuclear, ((screen_width - nuclear_rect[2]),0))
        screen.blit(nuclear, (0,(screen_height - nuclear_rect[3])))


    # if all zombies are killed
    if not zombiegroup:

        # give new power up to player
        
        # set new spawners at specific wave points
        if wave == 5:
            spawners = 2
        elif wave == 10:
            spawners = 3
        elif wave == 15:
            spawners = 4

        # add delay between waves
        if wave_delay == wave_delay_max:
            wave += 1
            # spawn new zombies
            for i in range(wave):
                zombie = Zombie()
                which_spawner = random.randrange(0,spawners)
                if which_spawner == 2:
                    zombie.rect.x = random.randint(screen_width - nuclear_rect[2],
                                                   screen_width)
                    zombie.rect.y = random.randint(0,nuclear_rect[3])
                elif which_spawner == 3:
                    zombie.rect.x = random.randint(0,nuclear_rect[2])
                    zombie.rect.y = random.randint(screen_height - nuclear_rect[3],
                                                   screen_height)
                elif which_spawner == 1:
                    zombie.rect.x = random.randint(screen_width - nuclear_rect[2],
                                                   screen_width)
                    zombie.rect.y = random.randint(screen_height - nuclear_rect[3],
                                                   screen_height)
                else:
                    zombie.rect.x = random.randint(0,nuclear_rect[2])
                    zombie.rect.y = random.randint(0,nuclear_rect[3])
                    
                allgroup.add(zombie)
                zombiegroup.add(zombie)
                wave_delay = 0
        
        else:
            wave_delay += 1
            
        # Spawn power up at half of wave delay
        if wave_delay == wave_delay_max/2 and not powerup_group:
            powerup = PowerBomb()
            powerup.rect.x = 0
            powerup.rect.y = screen_height/2 - powerup.rect[3]
            allgroup.add(powerup)
            powerup_group.add(powerup)

    # draw all sprites to screen
    allgroup.draw(screen)

    # display health
    healthbar.display()

    # display score
    scoreSurface = deluxeFont.render(("Score: " + str(score)), False,
                                     (51,255,51))
    waveSurface = deluxeFont.render(("Wave: " + str(wave)), False,
                                    (255,255,255))
    screen.blit(scoreSurface,((screen_width/2) - (scoreSurface.get_width()/2) - waveSurface.get_width(),
                              healthbar.image.get_height()))
    screen.blit(waveSurface,((screen_width/2) - (scoreSurface.get_width()/2) + scoreSurface.get_width(),
                              healthbar.image.get_height()))

    # display fps
    fpsSurface = deluxeFont.render(str(clock.get_fps()), False, (255,255,255))
    screen.blit(fpsSurface,((screen_width/2)-(fpsSurface.get_width()/2),
                            screen_height - fpsSurface.get_height()))

    # end game if shooter health is 0 or lower
    if shooter.health <= 0:
        done = True

    # refresh screen
    pygame.display.flip()


