import pygame
import random
#
pygame.init()

# Screen setup
WIDTH, HEIGHT = 672, 768
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Space Invaders")

BLACK = (0, 0, 0)

# Invader Class
class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        super().__init__()
        # loads image and scales to the same size as before
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
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
class Defender(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("defender.png").convert_alpha() #loads the defender sprite

        # Scales the sprite to the correct size
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 5

    def update(self, keys): #reads keyboard inputs
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Prevents the defender to leave the screen bounderies
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
class InvaderBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
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

all_sprites = pygame.sprite.Group()
invader_bullets = pygame.sprite.Group()

# 2D array of invaders
ROWS = 5
COLS = 8

SPACING_X = 60
SPACING_Y = 55
START_X = 80
START_Y = 80

invaders = []
all_sprites = pygame.sprite.Group()

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
        all_sprites.add(inv)
    invaders.append(row_list)

#creates the player
player = Defender(WIDTH // 2, HEIGHT - 20)
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
clock = pygame.time.Clock() # adds clock object to allow for the controlling of game speed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #player movement
    keys = pygame.key.get_pressed()
    player.update(keys)
    
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

    # Defender gets = game over
    if pygame.sprite.spritecollide(player, invader_bullets, True):
        running = False
        print("GAME OVER You have died.")

    # Creates frame
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(45) # game speed in fps

pygame.quit()


