#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from Code.Level import Level
from Code.Menu import Menu
from Code.Score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self, ):

        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            return_menu = menu.run()

            if return_menu in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                player_score = [0, 0]
                level = Level(self.window, 'Level1', return_menu, player_score)
                level_return = level.run(player_score)
                if level_return:
                    level = Level(self.window, 'Level2', return_menu, player_score)
                    level_return = level.run(player_score)
                    if level_return:
                        score.save(return_menu, player_score)

            elif return_menu == MENU_OPTION[3]:
                score.show()

            elif return_menu == MENU_OPTION[4]:
                pygame.quit()  # Close window
                quit()  # End Pygame
