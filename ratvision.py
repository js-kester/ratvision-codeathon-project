import pygame
import tkinter
from tkinter import messagebox
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576
# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False

    def __init__(self, x, y, filename):
        # Call the parent class (sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Load image which will be for the animation
        img = pygame.image.load("rat.png").convert()
        # Create the animations objects
        self.move_right_animation = Animation(img, 32, 32)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), 32, 32)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), 32, 32)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), 32, 32)
        # Load explosion image
        img = pygame.image.load("ratexplode2.png").convert()
        self.explosion_animation = Animation(img, 30, 30)
        # Save the player image
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self, horizontal_blocks, vertical_blocks):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # This will stop the user for go up or down when it is inside of the box

            for block in pygame.sprite.spritecollide(self, horizontal_blocks, False):
                self.rect.centery = block.rect.centery
                self.change_y = 0
            for block in pygame.sprite.spritecollide(self, vertical_blocks, False):
                self.rect.centerx = block.rect.centerx
                self.change_x = 0

            # This will cause the animation to start

            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() - 1:
                pygame.time.wait(500)
                self.game_over = True
            self.explosion_animation.update(5)
            self.image = self.explosion_animation.get_current_image()

    def move_right(self):
        self.change_x = 3

    def move_left(self):
        self.change_x = -3

    def move_up(self):
        self.change_y = -3

    def move_down(self):
        self.change_y = 3

    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image, True, False)
        self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image, 270)
        self.change_y = 0


class Animation(object):
    def __init__(self, img, width, height):
        # Load the sprite sheet
        self.sprite_sheet = img
        # Create a list to store the images
        self.image_list = []
        self.load_images(width, height)
        # Create a variable which will hold the current image of the list
        self.index = 0
        # Create a variable that will hold the time
        self.clock = 1

    def load_images(self, width, height):
        # Go through every single image in the sprite sheet
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                # load images into a list
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # Assuming black works as the transparent color
        image.set_colorkey((0, 0, 0))
        # Return the image
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Increase index
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # Draw the ellipse
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the direction of the slime
        self.change_x = change_x
        self.change_y = change_y
        # Load image
        self.image = pygame.image.load("ratstill.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # **********************************************************************************#
        self.infected = False
        self.wait = 0
        self.image = pygame.image.load("ratstill.png").convert()
        img = pygame.image.load("personwalk.png").convert()
        # Create the animations objects
        self.move_left_animation = Animation(img, 30, 30)
        self.move_right_animation = Animation(pygame.transform.flip(img, True, False), 30, 30)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 90), 30, 30)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 270), 30, 30)
        self.player_image = pygame.image.load("ratstill.png").convert()
        self.player_image.set_colorkey(BLACK)
        # **********************************************************************************#

    def update(self, horizontal_blocks, vertical_blocks):
        if self.infected and self.wait < 100:
            self.wait += 1
            return

        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        direction = random.choice(("left", "right", "up", "down"))
        if self.rect.topleft in self.get_intersection_position():
            if direction == "left" and self.change_x == 0:
                self.change_x = -1 * random.randint(2, 4)
                self.change_y = 0
                # *******************
                self.move_left_animation.update(3)
                self.image = self.move_left_animation.get_current_image()
                # *********************
            elif direction == "right" and self.change_x == 0:
                self.change_x = random.randint(2, 4)
                self.change_y = 0
                # *******************
                self.move_right_animation.update(3)
                self.image = self.move_right_animation.get_current_image()
                # *********************
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -1 * random.randint(2, 4)
                # *******************
                self.move_up_animation.update(3)
                self.image = self.move_up_animation.get_current_image()
                # *********************
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = random.randint(2, 4)
                # *******************
                self.move_down_animation.update(3)
                self.image = self.move_down_animation.get_current_image()
                # *********************
        # *************************************************************
        else:
            if self.change_x > 0:
                self.move_right_animation.update(3)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(3)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(3)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(3)
                self.image = self.move_up_animation.get_current_image()
            # *********************
        # *************************************************************

    def infect(self):
        self.infected = True
        self.image = pygame.image.load("zombiestill.png").convert()
        self.image.set_colorkey(BLACK)
        img = pygame.image.load("zombiewalk.png").convert()
        # Create the animations objects
        self.move_right_animation = Animation(img, 34, 30)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), 34, 30)
        self.move_up_animation = Animation(pygame.transform.rotate(img, 90), 30, 34)
        self.move_down_animation = Animation(pygame.transform.rotate(img, 270), 30, 34)

    def get_intersection_position(self):
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 3:
                    items.append((j * 32, i * 32))

        return items


def enviroment():
    grid = ((0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0),
            (0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0))

    return grid


def draw_enviroment(screen):
    for i, row in enumerate(enviroment()):
        for j, item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, WHITE, [j * 32, i * 32], [j * 32 + 32, i * 32], 3)
                pygame.draw.line(screen, WHITE, [j * 32, i * 32 + 32], [j * 32 + 32, i * 32 + 32], 3)
            elif item == 2:
                pygame.draw.line(screen, WHITE, [j * 32, i * 32], [j * 32, i * 32 + 32], 3)
                pygame.draw.line(screen, WHITE, [j * 32 + 32, i * 32], [j * 32 + 32, i * 32 + 32], 3)


class Animation(object):
    def __init__(self, img, width, height):
        # Load the sprite sheet
        self.sprite_sheet = img
        # Create a list to store the images
        self.image_list = []
        self.load_images(width, height)
        # Create a variable which will hold the current image of the list
        self.index = 0
        # Create a variable that will hold the time
        self.clock = 1

    def load_images(self, width, height):
        # Go through every single image in the sprite sheet
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                # load images into a list
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # Assuming black works as the transparent color
        image.set_colorkey((0, 0, 0))
        # Return the image
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Increase index
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0

class Game(object):
    def __init__(self, extra):
        self.font = pygame.font.Font(None, 40)
        self.about = False
        self.game_over = True
        self.won = False
        self.lost = False
        self.wait = 0
        self.extra = extra
        self.redo = True
        # Create the variable for the score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None, 35)
        # Create the menu of the game
        self.menu = Menu(("Start", "About", "Exit"), font_color=WHITE, font_size=60)
        self.win_screen = Menu(("You Infected Everyone! :)",), font_color=WHITE, font_size=60)
        # self.lose_screen = Menu(("The Infection Killed You!",), font_color=WHITE, font_size=60)
        # Create the player
        self.player = Player(32, 128, "ratstill.png")
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Set the environment:
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
        # Create the enemies
        self.enemies = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.people.add(Slime(288, 96, 0, 2))
        self.people.add(Slime(288, 320, 0, -2))
        self.people.add(Slime(544, 128, 0, 2))
        self.people.add(Slime(32, 224, 0, 2))
        self.people.add(Slime(160, 64, 2, 0))
        self.people.add(Slime(448, 64, -2, 0))
        self.people.add(Slime(640, 448, 2, 0))
        self.people.add(Slime(448, 320, 2, 0))
        self.people.add(Slime(288, 320, 2, 0))
        self.people.add(Slime(448, 320, 2, 0))
        for i in range(self.extra):
            self.people.add(Slime(448, 320, 2, 0))

    def process_events(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about and not self.won:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.__init__(self.extra + (not self.redo))
                            self.game_over = False
                        elif self.menu.state == 1:
                            # --- ABOUT ------
                            self.about = True
                        elif self.menu.state == 2:
                            # --- EXIT -------
                            # User clicked exit
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            self.people.update(self.horizontal_blocks, self.vertical_blocks)

            for p in self.people.sprites():
                if p.wait >= 100:
                    self.enemies.add(p)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.people, False)
            block_hit_list2 = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if len(block_hit_list) > 0:
                for p in block_hit_list:
                    if not p.infected:
                        p.infect()
                        self.score += 1
                        if self.score == (10 + self.extra):
                            self.won = True
            if len(block_hit_list2) > 0:
                self.player.explosion = True
                self.score = 0

            self.game_over = self.player.game_over

    def display_frame(self, screen):
        # First, clear the screen to white. Don't put other drawing commands
        screen.fill(BLACK)
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                self.display_message(screen, "Rat")
            else:
                self.menu.display_frame(screen)
        elif self.won:
            screen.fill(BLACK)
            self.win_screen.display_frame(screen)
            if self.wait < 100:
                self.wait += 1
            else:
                self.wait = 0
                self.won = False
                self.game_over = True
                self.redo = False
        else:
            # --- Draw the game here ---
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.people.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            # Render the text for the score
            text = self.font.render(f"Infected: {self.score}/{self.extra + 10}", True, GREEN)
            # Put the text on the screen
            screen.blit(text, [120, 20])

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def display_message(self, screen, message, color=(255, 0, 0)):
        label = self.font.render(message, True, color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (SCREEN_WIDTH / 2) - (width / 2)
        posY = (SCREEN_HEIGHT / 2) - (height / 2)
        # Draw the label onto the screen
        screen.blit(label, (posX, posY))


class Menu(object):
    state = 0

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        label = self.font.render("Rat Vision", True, (0, 255, 0))
        posX = (SCREEN_WIDTH / 2) - (label.get_width() / 2)
        posY = (SCREEN_HEIGHT / 4) - (label.get_height() / 2)
        screen.blit(label, (posX, posY))
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1

def main():
    # Initialize all imported pygame modules
    pygame.init()
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Set the current window caption
    pygame.display.set_caption("Rat Vision")
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Create a game object
    game = Game(0)
    # -------- Main Program Loop -----------
    while not done:
        # --- Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        # --- Game logic should go here
        game.run_logic()
        # --- Draw the current frame
        game.display_frame(screen)
        # --- Limit to 30 frames per second
        clock.tick(30)
    # Close the window and quit.
    pygame.quit()

if __name__ == '__main__':
    main()
