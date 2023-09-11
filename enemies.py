import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


class Ellipse(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        # Draw the ellipse
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        
class Slime(pygame.sprite.Sprite):
    def __init__(self,x,y,change_x,change_y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the direction of the slime
        self.change_x = change_x
        self.change_y = change_y
        # Load image
        self.image = pygame.image.load("ratstill.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
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

    def update(self,horizontal_blocks,vertical_blocks):
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

        direction = random.choice(("left","right","up","down"))
        if self.rect.topleft in self.get_intersection_position():
            if direction == "left" and self.change_x == 0:
                self.change_x = -1 * random.randint(2,4)
                self.change_y = 0
                # *******************
                self.move_left_animation.update(3)
                self.image = self.move_left_animation.get_current_image()
                # *********************
            elif direction == "right" and self.change_x == 0:
                self.change_x = random.randint(2,4)
                self.change_y = 0
                # *******************
                self.move_right_animation.update(3)
                self.image = self.move_right_animation.get_current_image()
                # *********************
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -1 * random.randint(2,4)
                # *******************
                self.move_up_animation.update(3)
                self.image = self.move_up_animation.get_current_image()
                # *********************
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = random.randint(2,4)
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
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 3:
                    items.append((j*32,i*32))

        return items
    
        
def enviroment():
    grid = ((0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3,1,1,1,1,1,3,1),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0),
            (0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0))

    return grid

def draw_enviroment(screen):
    for i,row in enumerate(enviroment()):
        for j,item in enumerate(row):
            if item == 1:
                pygame.draw.line(screen, WHITE , [j*32, i*32], [j*32+32,i*32], 3)
                pygame.draw.line(screen, WHITE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2:
                pygame.draw.line(screen, WHITE , [j*32, i*32], [j*32,i*32+32], 3)
                pygame.draw.line(screen, WHITE , [j*32+32, i*32], [j*32+32,i*32+32], 3)


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
