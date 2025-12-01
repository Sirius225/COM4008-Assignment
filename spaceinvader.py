import pygame as pg
import random

pg.init()

# Screen setup
WIDTH, HEIGHT = 672, 768
screen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Space Invaders")
clock = pg.time.Clock() # adds clock object to allow for the controlling of game speed

BLACK = (0, 0, 0)



class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("defender.png").convert()
        self.image = pg.transform.scale(self.image, (50, 38))#to generate the size of the player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2. #player spawning point
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.lives = 3 #number of lives
        self.hidden = False #to check if the player is hidden when hit by invader bullet
        self.hide_timer = 2 #timer for hiding the player

    def update(self):
        self.speedx = 0 #speed of sprite initially
# sprite movement and speed
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH #prevents the player from going out side the screen
        if self.rect.left < 0:
            self.rect.left = 0


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)      

class Bullet(pg.sprite.Sprite):
  def __init__(self, x, y):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load("laserBlue13.png").convert()
    self.image = pg.transform.scale(self.image, (50, 38))
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.bottom = y
    self.rect.centerx = x
    self.speedy = -10

  def update(self):
    self.rect.y += self.speedy
    #kill if it moves off the top of the screen
    if self.rect.bottom < 0:
        self.kill()


 
bullets = pg.sprite.Group()#object is created
       
# Invader Class
class Invader(pg.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        # loads image and scales to the same size as before
        self.image = pg.image.load(image_file).convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


# Subclasses 
class Squid(Invader):   # Invader1
    def __init__(self, x, y):
        super().__init__(x, y, "invader1.png")


class Crab(Invader):    # Invader2
    def __init__(self, x, y):
        super().__init__(x, y, "invader2.png")


class Octopus(Invader): # Invader3
    def __init__(self, x, y):
        super().__init__(x, y, "invader3.png")


#Defender class
"""class Defender(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("defender.png").convert_alpha() #loads the defender sprite

        # Scales the sprite to the correct size
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 5

    def update(self, keys): #reads keyboard inputs
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed

        # Prevents the defender to leave the screen bounderies
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
"""            
class InvaderBullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((4, 12))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

#Invaders speed up when destroyed
INVADER_SPEED_MULTIPLIER = 1.05

def remove_invader(inv):
    global speed_x
    inv.kill()
    speed_x *= INVADER_SPEED_MULTIPLIER

all_sprites = pg.sprite.Group()
invader_bullets = pg.sprite.Group()

# 2D array of invaders
ROWS = 5
COLS = 8

SPACING_X = 60
SPACING_Y = 55
START_X = 80
START_Y = 80

invaders = []
all_sprites = pg.sprite.Group()
invader_group = pg.sprite.Group()

for row in range(ROWS):
    row_list = []
    for col in range(COLS):
        x = START_X + col * SPACING_X
        y = START_Y + row * SPACING_Y

        if row == 0:
            inv = Squid(x, y)            # 1 row of Squid
        elif row in (1, 2):
            inv = Crab(x, y)             # 2 rows of Crab
        else:
            inv = Octopus(x, y)          # 2 rows of Octopus

        row_list.append(inv)
        invader_group.add(inv)
        all_sprites.add(inv)
    invaders.append(row_list)

#creates the player
bullets = pg.sprite.Group()
player = Player()
all_sprites.add(player)


# Movement
speed_x = 1
move_down_amount = 20

SHOOT_CHANCE = 0.001

def get_edges(): # This gets the information of the leftmost and rightmost invaders to allow the group to shift down when they touch the edge of the screen
    left = min(inv.rect.left for row in invaders for inv in row)
    right = max(inv.rect.right for row in invaders for inv in row)
    return left, right


# The game Loop

running = True
clock = pg.time.Clock() # adds clock object to allow for the controlling of game speed

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
    #player movement
    all_sprites.update()
    
    left_edge, right_edge = get_edges() #Finds the leftmost and rightmost invaders in the array
    shift_down = False

    # When any invader hits the wall it reverses the direction and moves down the sprites
    if right_edge >= WIDTH - 10: #invader hits right side shifts down and starts to move left. -10 allows for them to not visually stick to the wall
        speed_x = -speed_x
        shift_down = True
    elif left_edge <= 10: #invader hits left side shifts down and starts to move right
        speed_x = -speed_x
        shift_down = True

    # If the invaders hit a wall they will shift down.
    for row in invaders:
        for inv in row:
            if shift_down:
                inv.move(0, move_down_amount) #shifts down the invaders
            inv.move(speed_x, 0) #This will then make them move either left or right

    for row in invaders:
        for inv in row:
            if inv.rect.bottom >= player.rect.top: #checks when the invaders touch the bottom of the screen
                running = False #end the game
                print("GAME OVER")

    # Invaders shooting
    for row in invaders:
        for inv in row:
            if random.random() < SHOOT_CHANCE:
                bullet = InvaderBullet(inv.rect.centerx, inv.rect.bottom)
                invader_bullets.add(bullet)
                all_sprites.add(bullet)

    # Update bullets
    invader_bullets.update()

  # check to see if bullet hit an invader
    hits = pg.sprite.groupcollide(invader_group, bullets, True, True)
    for invader, bullet_list in hits.items():
        remove_invader(invader)


    # Defender gets hits and loses a life
    if pg.sprite.spritecollide(player, invader_bullets, True):
        player.hide()
        player.lives -= 1
    # Check for game over
    if player.lives == 0:
        running = False
        print("GAME OVER You have died.")


    # Creates frame
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(45) # game speed in fps

pg.quit()


