#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from player import Player
from enemies import *
import tkinter
from tkinter import messagebox
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

class Game(object):
    def __init__(self,extra):
        self.font = pygame.font.Font(None,40)
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
        self.font = pygame.font.Font(None,35)
        # Create the menu of the game
        self.menu = Menu(("Start","About","Exit"),font_color = WHITE,font_size=60)
        self.win_screen = Menu(("You Infected Everyone! :)",), font_color=WHITE, font_size=60)
        # self.lose_screen = Menu(("The Infection Killed You!",), font_color=WHITE, font_size=60)
        # Create the player
        self.player = Player(32, 128, "ratstill.png")
        # Create the blocks that will set the paths where the player can go
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Set the environment:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        # Create the enemies
        self.enemies = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.people.add(Slime(288,96,0,2))
        self.people.add(Slime(288,320,0,-2))
        self.people.add(Slime(544,128,0,2))
        self.people.add(Slime(32,224,0,2))
        self.people.add(Slime(160,64,2,0))
        self.people.add(Slime(448,64,-2,0))
        self.people.add(Slime(640,448,2,0))
        self.people.add(Slime(448,320,2,0))
        self.people.add(Slime(288, 320, 2, 0))
        self.people.add(Slime(448, 320, 2, 0))
        for i in range(self.extra):
            self.people.add(Slime(448, 320, 2, 0))


    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
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
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            self.people.update(self.horizontal_blocks,self.vertical_blocks)

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

    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands
        screen.fill(BLACK)
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                self.display_message(screen,"Rat")
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
            screen.blit(self.player.image,self.player.rect)
            # Render the text for the score
            text = self.font.render(f"Infected: {self.score}/{self.extra + 10}",True,GREEN)
            # Put the text on the screen
            screen.blit(text,[120,20])
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def display_message(self,screen,message,color=(255,0,0)):
        label = self.font.render(message,True,color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)
        # Draw the label onto the screen
        screen.blit(label,(posX,posY))


class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font=None,font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        label = self.font.render("Rat Vision",True,(0,255,0))
        posX = (SCREEN_WIDTH / 2) - (label.get_width() / 2)
        posY = (SCREEN_HEIGHT / 4) - (label.get_height() / 2)
        screen.blit(label, (posX, posY))
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1
