#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from Code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, ENTITY_SHOT_DELAY, PLAYER_KEY_SHOOT
from Code.Entity import Entity
from Code.PlayerShot import PlayerShot


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self, ):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 2:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT - 2:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 2:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH - 2:
            self.rect.centerx += ENTITY_SPEED[self.name]
        pass

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx + 30, self.rect.centery))
