#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Entity import Entity
from Code.Level import Level
from Code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self, ):

        while True:
            menu = Menu(self.window)
            return_menu = menu.run()

            if return_menu in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                level = Level(self.window, 'Level1', return_menu)
                level_return = level.run()
            elif return_menu == MENU_OPTION[4]:
                pygame.quit()  # Close window
                quit()  # End Pygame
