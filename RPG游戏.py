import random
import sys
from tkinter import *
import numpy
import pygame
import pygame.font
from pygame.constants import K_LEFT, K_RIGHT, QUIT
from pygame.locals import *

from music_manager import MusicManager

pygame.mixer.pre_init(44100, 16, 2, 512)
pygame.init()

# Music and Sound
soundtrack = ["background_village.wav", "battle_music.wav", "gameover.wav"]
swordtrack = [pygame.mixer.Sound("sword1.wav"), pygame.mixer.Sound("sword2.wav")]
fsound = pygame.mixer.Sound("fireball_sound.wav")
enemy_die = pygame.mixer.Sound("enemy_die.wav")
player_get_hurt = pygame.mixer.Sound("player_get_hurt.wav")

# Setting up the music

mmanager = MusicManager()
mmanager.playsoundtrack(soundtrack[0], -1, 0.02)
# Setting up the display
# Declaring variables to be used through the program
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.1
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

# Create the display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# light shade of the button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_white = (255, 255, 255)
color_black = (0, 0, 0)

# defining a font
headingfont = pygame.font.SysFont("simsun", 40)
regularfont = pygame.font.SysFont('Corbel', 25)
smallerfont = pygame.font.SysFont('simsun', 16)
text = regularfont.render('LOAD', True, color_light)
# Run animation for the RIGHT
run_ani_R = [pygame.image.load("Player_Sprite_R.png").convert_alpha(),
             pygame.image.load("Player_Sprite2_R.png").convert_alpha(),
             pygame.image.load("Player_Sprite3_R.png").convert_alpha(),
             pygame.image.load("Player_Sprite4_R.png").convert_alpha(),
             pygame.image.load("Player_Sprite5_R.png").convert_alpha(),
             pygame.image.load("Player_Sprite6_R.png").convert_alpha(),
             pygame.image.load("Player_Sprite_R.png").convert_alpha()]

# Run animation for the LEFT
run_ani_L = [pygame.image.load("Player_Sprite_L.png").convert_alpha(),
             pygame.image.load("Player_Sprite2_L.png").convert_alpha(),
             pygame.image.load("Player_Sprite3_L.png").convert_alpha(),
             pygame.image.load("Player_Sprite4_L.png").convert_alpha(),
             pygame.image.load("Player_Sprite5_L.png").convert_alpha(),
             pygame.image.load("Player_Sprite6_L.png").convert_alpha(),
             pygame.image.load("Player_Sprite_L.png").convert_alpha()]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("Player_Sprite_R.png").convert_alpha(),
                pygame.image.load("Player_Attack_R.png").convert_alpha(),
                pygame.image.load("Player_Attack_R.png").convert_alpha(),
                pygame.image.load("Player_Attack_R.png").convert_alpha(),
                pygame.image.load("Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("Player_Attack2_R.png").convert_alpha(),
                pygame.image.load("Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("Player_Attack3_R.png").convert_alpha(),
                pygame.image.load("Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("Player_Attack4_R.png").convert_alpha(),
                pygame.image.load("Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("Player_Attack5_R.png").convert_alpha(),
                pygame.image.load("Player_Sprite_R.png").convert_alpha()]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("Player_Sprite_L.png").convert_alpha(),
                pygame.image.load("Player_Attack_L.png").convert_alpha(),
                pygame.image.load("Player_Attack_L.png").convert_alpha(),
                pygame.image.load("Player_Attack_L.png").convert_alpha(),
                pygame.image.load("Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("Player_Attack2_L.png").convert_alpha(),
                pygame.image.load("Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("Player_Attack3_L.png").convert_alpha(),
                pygame.image.load("Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("Player_Attack4_L.png").convert_alpha(),
                pygame.image.load("Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("Player_Attack5_L.png").convert_alpha(),
                pygame.image.load("Player_Sprite_L.png").convert_alpha()]

# Animations for the Health Bar
health_ani = [pygame.image.load("heart0.png").convert_alpha(),
              pygame.image.load("heart.png").convert_alpha(),
              pygame.image.load("heart2.png").convert_alpha(),
              pygame.image.load("heart3.png").convert_alpha(),
              pygame.image.load("heart4.png").convert_alpha(),
              pygame.image.load("heart5.png").convert_alpha()]


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png").convert_alpha()
        self.rectBGimg = self.bgimage.get_rect()
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png").convert_alpha()
        self.rect = self.image.get_rect(center=(350, 350))
        self.bgX1 = 0
        self.bgY1 = 285

    def render(self):
        displaysurface.blit(self.image, (self.bgX1, self.bgY1))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Position and direction
        self.qua = 10
        self.pos = vec((40, 140))
        self.vel = vec(30, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"
        self.rect.center = self.pos
        self.forcex = 0
        self.forcey = 0

        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0

        # Combat
        self.attacking = False
        self.cooldown = False
        self.immune = False
        self.special = False
        self.experiance = 0
        self.attack_frame = 0
        self.healths = 5
        self.magic_cooldown = 1
        self.mana = 0
        self.money = 0

        # Sound
        self.slash = 0

    def move(self):
        if cursor.wait == 1:
            return
        # Keep a constant acceleration of 0.5 in the downwards direction (gravity)
        self.acc = vec(0, 0.5)

        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

            # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

        # This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if 1 <= self.attack_frame < 20 and self.direction == "LEFT" and self.attacking == True:
            #self.pos.x -= 28
            self.rect.bottomright = self.pos  # Update rect with new pos
            #self.pos.x += 28
        else:
            self.rect.midbottom = self.pos

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.rect.bottom >= lowest.rect.top:
                    self.rect.y = lowest.rect.top - self.rect.height + 1
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def update(self):
        if cursor.wait == 1:
            return
        # Return to base frame if at end of movement sequence
        if self.move_frame > 6:
            self.move_frame = 0
            return

        # Move the character to the next frame if conditions are met
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        if cursor.wait == 1:
            return
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > 20:
            self.attack_frame = 0
            self.attacking = False

        if self.attack_frame == 0:
            mmanager.playsound(swordtrack[self.slash], 0.05)

            self.slash += 1
            if self.slash >= 2:
                self.slash = 0

        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.image = attack_ani_L[self.attack_frame]

            # Update the current attack frame
        self.attack_frame += 1

    def jump(self):
        self.rect.y += 1

        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.y -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.pos.x -= 28
        if self.attack_frame == 20:
            self.pos.x += 28

    def player_hit(self):
        if not self.cooldown:
            self.cooldown = True  # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

            self.healths = self.healths - 1
            health.image = health_ani[self.healths]
            mmanager.playsound(player_get_hurt, 0.1)
            if self.healths <= 0:
                self.kill()
                mmanager.stop()
                mmanager.playsoundtrack(soundtrack[2], -1, 0.1)
                pygame.display.update()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)

        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 2  # Randomised velocity of the generated enemy
        self.mana = random.randint(1, 3)

        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235

    def move(self):
        if cursor.wait == 1:
            return
        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        # Updates positon with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect

    def update(self):
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)

        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)

        # Activates upon either of the two expressions being true
        if hits and player.attacking == True or f_hits:
            self.kill()
            mmanager.playsound(enemy_die, 0.05)
            handler.dead_enemy_count += 1

            if player.mana < 1000:
                player.mana += self.mana  # Release mana
            player.experiance += 1  # Release expeiriance

            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if 0 <= rand_num < 30:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif 30 <= rand_num < 100:
                item_no = 2

            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y

        # If collision has occured and player not attacking, call "hit" function
        elif hits and player.attacking == False:
            player.player_hit()

    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))


class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.wait = 0
        self.wait_status = False
        self.turning = 0

        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon

        if self.direction == 0:
            self.image = pygame.image.load("enemy2_R.png").convert_alpha()
        if self.direction == 1:
            self.image = pygame.image.load("enemy2_L.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250

    def direction_check(self):
        if player.pos.x - self.pos.x < 0 and self.direction == 0:
            return 1
        if player.pos.x - self.pos.x > 0 and self.direction == 1:
            return 1

    def turn(self):
        if self.wait > 0:
            self.wait -= 1
            return
        elif int(self.wait) <= 0:
            self.turning = 0

        if self.direction:
            self.direction = 0
            self.image = pygame.image.load("enemy2_R.png").convert_alpha()
        else:
            self.direction = 1
            self.image = pygame.image.load("enemy2_L.png").convert_alpha()

    def move(self):
        if cursor.wait == 1:
            return
        if self.turning == 1:
            self.turn()
            return

        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        if self.wait > 60:
            self.wait_status = True
        elif int(self.wait) <= 0:
            self.wait_status = False

        if self.direction_check():
            self.turn()
            self.wait = 90
            self.turning = 1

        if self.wait_status:
            rand_num = numpy.random.uniform(0, 60)
            if int(rand_num) == 30:
                bolt1 = Bolt(self.pos.x, self.pos.y, self.direction)
                Bolts.add(bolt1)
            self.wait -= 1
        elif self.direction == 0:
            self.pos.x += self.vel.x
            self.wait += self.vel.x
        elif self.direction == 1:
            self.pos.x -= self.vel.x
            self.wait += self.vel.x

        self.rect.center = self.pos  # Updates rect

    def update(self):
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)

        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)

        # Activates upon either of the two expressions being true
        if hits and player.attacking == True or f_hits:
            self.kill()
            mmanager.playsound(enemy_die, 0.05)
            handler.dead_enemy_count += 1

            if player.mana < 200:
                player.mana += self.mana  # Release mana
            player.experiance += 1  # Release expeiriance

            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if 0 <= rand_num < 50:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif 50 <= rand_num < 100:
                item_no = 2

            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y

    def render(self):
        # Displays the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))


class Bolt(pygame.sprite.Sprite):
    def __init__(self, x, y, d):
        super().__init__()
        self.image = pygame.image.load("bolt.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x + 15
        self.rect.y = y + 20
        self.direction = d

    def fire(self):
        # Runs while the fireball is still within the screen w/ extra margin
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = pygame.image.load("bolt.png")
                displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("bolt.png")
                displaysurface.blit(self.image, self.rect)

            if self.direction == 0:
                self.rect.move_ip(12, 0)
            else:
                self.rect.move_ip(-12, 0)
        else:
            self.kill()

        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        if hits:
            player.player_hit()
            self.kill()


class EventHandler:
    def __init__(self):
        self.root = None
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 2
        self.enemy_generation2 = pygame.USEREVENT + 3
        self.stage = 0
        self.world = 0
        self.stage_enemies = []
        self.stage_enemies.append(0)
        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 / 2) + 1))
        print(self.stage_enemies)

    def stage_handler(self):
        # Code for the Tkinter stage selection window
        self.root = Tk()
        self.root.geometry('200x170')

        button1 = Button(self.root, text="Twilight Dungeon", width=18, height=2,
                         command=self.world1)
        button2 = Button(self.root, text="Skyward Dungeon", width=18, height=2,
                         command=self.world2)
        button3 = Button(self.root, text="Hell Dungeon", width=18, height=2,
                         command=self.world3)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)

        self.root.mainloop()

    def world1(self):
        self.root.destroy()
        self.stage = 1
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.world = 1
        button.imgdisp = 1
        castle.hide = True
        self.battle = True

        mmanager.playsoundtrack(soundtrack[1], -1, 0.02)

    def world2(self):
        self.root.destroy()
        self.stage = 1
        background.bgimage = pygame.image.load("desert.jpg").convert_alpha()
        ground.image = pygame.image.load("desert_ground.png").convert_alpha()
        pygame.time.set_timer(self.enemy_generation2, 2500)
        self.world = 2
        button.imgdisp = 1
        castle.hide = True
        self.battle = True

        mmanager.playsoundtrack(soundtrack[1], -1, 0.02)

    def world3(self):
        self.root.destroy()
        self.stage = 1

        self.world = 3
        mmanager.playsoundtrack(soundtrack[1], -1, 0.02)
        button.imgdisp = 1
        castle.hide = True
        self.battle = True

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        pygame.time.set_timer(self.enemy_generation2, 0)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 0
        self.world = 0

        # Destroy any enemies or items lying aroundN
        for group in Enemies, Items:
            for entity_and_item in group:
                entity_and_item.kill()

        # Bring back normal backgrounds
        stage_display.clear = False
        castle.hide = False
        background.bgimage = pygame.image.load("Background.png").convert_alpha()
        ground.image = pygame.image.load("Ground.png").convert_alpha()

    def next_stage(self):  # Code for when the next stage is clicked
        button.imgdisp = 1
        self.stage += 1
        print("Stage: " + str(self.stage))
        self.enemy_count = 0
        self.dead_enemy_count = 0
        if self.world == 1:
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
        elif self.world == 2:
            pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage))

    def update(self):
        if self.dead_enemy_count == self.stage_enemies[self.stage] and self.stage != 0:
            stage_display.clear = True
            stage_display.stage_clear()


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png").convert_alpha()

    def render(self):
        displaysurface.blit(self.image, (10, 10))


class StageDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text = headingfont.render("STAGE: " + str(handler.stage), True, color_dark)
        self.rect = self.text.get_rect()
        self.posx = -100
        self.posy = 100
        self.display = False
        self.clear = False

    def move_display(self):
        # Create the text to be displayed
        self.text = headingfont.render("第" + str(handler.stage) + "关", True, color_dark)
        if self.posx < 720:
            self.posx += 5
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.posx = -100
            self.posy = 100

    def stage_clear(self):
        button.imgdisp = 0
        self.text = headingfont.render("清关!", True, color_dark)
        if self.posx < 720:
            self.posx = 280
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.clear = False
            self.posx = -100
            self.posy = 100


class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((120, 100))
        self.rect = self.surf.get_rect(center=(500, 10))
        self.health_text = smallerfont.render("Health: ", True, color_white)

    @staticmethod
    def update_draw():
        # Create the text to be displayed
        text1 = smallerfont.render("关卡: " + str(handler.stage), True, color_white)
        text2 = smallerfont.render("经验: " + str(player.experiance), True, color_white)
        text3 = smallerfont.render("魔力: " + str(player.mana), True, color_white)
        text4 = smallerfont.render("帧数: " + str(int(FPS_CLOCK.get_fps())), True, color_white)
        text5 = smallerfont.render("金钱: " + str(int(player.money)), True, color_white)
        text6 = smallerfont.render(
            "剩余敌人: " + str(int(handler.stage_enemies[handler.stage] - handler.dead_enemy_count)), True,
            color_black)

        # Draw the text to the status bar
        displaysurface.blit(text1, (585, 7))
        displaysurface.blit(text2, (585, 27))
        displaysurface.blit(text3, (585, 47))
        displaysurface.blit(text4, (585, 67))
        displaysurface.blit(text5, (585, 87))
        displaysurface.blit(text6, (400, 9))


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("castle.png")

    def update(self):
        if not self.hide:
            displaysurface.blit(self.image, (400, 80))


class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype):
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("heart.png")
        elif itemtype == 2:
            self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0

    def render(self):
        self.rect.x = self.posx
        self.rect.y = self.posy
        displaysurface.blit(self.image, self.rect)

    def update(self):
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        # Code to be activated if item comes in contact with player
        if hits:
            if player.healths < 5 and self.type == 1:
                player.healths += 1
                health.image = health_ani[player.healths]
                self.kill()
            if self.type == 2:
                player.money += 1
                self.kill()


class PButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.vec = vec(620, 300)
        self.imgdisp = 0

    def render(self, num):
        if num == 0:
            self.image = pygame.image.load("home_small.png").convert_alpha()
        elif num == 1:
            if cursor.wait == 0:
                self.image = pygame.image.load("pause_small.png").convert_alpha()
            else:
                self.image = pygame.image.load("play_small.png").convert_alpha()

        displaysurface.blit(self.image, self.vec)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cursor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.wait = 0

    def pause(self):
        if self.wait == 1:
            self.wait = 0
        else:
            self.wait = 1

    def hover(self):
        if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
            pygame.mouse.set_visible(False)
            self.rect.center = pygame.mouse.get_pos()  # update position
            displaysurface.blit(self.image, self.rect)
        else:
            pygame.mouse.set_visible(True)


class FireBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = player.direction
        if self.direction == "RIGHT":
            self.image = pygame.image.load("fireball1_R.png")
        else:
            self.image = pygame.image.load("fireball1_L.png")
        self.rect = self.image.get_rect(center=player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40

    def fire(self):
        player.magic_cooldown = 0
        # Runs while the fireball is still within the screen w/ extra margin
        if -10 < self.rect.x < 710:
            if self.direction == "RIGHT":
                self.image = pygame.image.load("fireball1_R.png")
                displaysurface.blit(self.image, self.rect)
                self.rect.move_ip(12, 0)
            else:
                self.image = pygame.image.load("fireball1_L.png")
                displaysurface.blit(self.image, self.rect)
                self.rect.move_ip(-12, 0)
        else:
            self.kill()
            player.magic_cooldown = 1
            player.attacking = False


Enemies = pygame.sprite.Group()
player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

background = Background()
ground = Ground()
cursor = Cursor()
button = PButton()

ground_group = pygame.sprite.Group()
ground_group.add(ground)

castle = Castle()
handler = EventHandler()
health = HealthBar()
stage_display = StageDisplay()
status_bar = StatusBar()
Fireballs = pygame.sprite.Group()
Items = pygame.sprite.Group()
Bolts = pygame.sprite.Group()

hit_cooldown = pygame.USEREVENT + 1

while 1:
    player.gravity_check()
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == hit_cooldown:
            player.cooldown = False
        # Will run when the close window button is clicked
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[handler.stage]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
        if event.type == handler.enemy_generation2:
            if handler.enemy_count < handler.stage_enemies[handler.stage]:
                if handler.enemy_count % 2:
                    enemy = Enemy2()
                else:
                    enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
        # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                if button.imgdisp == 1:
                    cursor.pause()
                elif button.imgdisp == 0:
                    handler.home()

        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if event.key == pygame.K_m and player.magic_cooldown == 1 and player.healths > 0:
                if player.mana >= 6:
                    player.mana -= 6
                    player.attacking = True
                    fireball = FireBall()
                    Fireballs.add(fireball)
                    mmanager.playsound(fsound, 0.3)
            if event.key == pygame.K_n:
                handler.dead_enemy_count = 0
                if handler.battle == True and len(Enemies) == 0:
                    handler.next_stage()
                    stage_display = StageDisplay()
                    stage_display.display = True
            if event.key == pygame.K_q and 400 < player.rect.x < 600:
                handler.stage_handler()
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_RETURN:
                if not player.attacking:
                    player.attacking = True

    # Player related functions
    player.update()
    if player.attacking:
        player.attack()
    player.move()

    # Display and Background related functions
    background.render()
    ground.render()
    button.render(button.imgdisp)
    cursor.hover()

    # Render stage display
    if stage_display.display:
        stage_display.move_display()
    if stage_display.clear:
        stage_display.stage_clear()
    # Rendering Sprites
    castle.update()
    if player.healths > 0:
        displaysurface.blit(player.image, player.rect)
    health.render()

    # Render Status Bar
    displaysurface.blit(status_bar.surf, (580, 5))
    status_bar.update_draw()
    handler.update()

    for i in Items:
        i.render()
        i.update()

    for ball in Fireballs:
        ball.fire()

    for bolt in Bolts:
        bolt.fire()

    for entity in Enemies:
        entity.update()
        entity.move()
        entity.render()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
