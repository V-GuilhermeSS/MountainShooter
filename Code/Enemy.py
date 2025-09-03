#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import pygame

from Code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY, SHOT_SOUNDS
from Code.EnemyShot import EnemyShot
from Code.Entity import Entity
from Code.Explosion import Explosion


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.explosion: Explosion | None = None
        self.score_given = False  # garante que a pontuação seja somada apenas 1 vez
        self.name = name
        self.shoot_sound = pygame.mixer.Sound(SHOT_SOUNDS.get(self.name))
        self.has_shot_once = False
        self.shot_delay = 10
        self.active_shots = []
        self.explosion_sound = pygame.mixer.Sound('./asset/8bit_bomb_explosion.wav')

    def move(self):
        if self.health > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        else:
            if not self.explosion:
                self.explosion_sound.play()
                self.explosion = Explosion(position=self.rect.center, scale=1.0, frame_delay=4, name=self.name)
            else:
                self.explosion.update()

    def shoot(self):
        if self.health <= 0:
            return None

        self.shot_delay -= 1

        if self.shot_delay <= 0:
            if not self.has_shot_once:
                self.has_shot_once = True
            else:
                max_delay = ENTITY_SHOT_DELAY[self.name]
                self.shot_delay = random.choice([max_delay, max_delay // 2])

            self.shoot_sound.play()
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

        return None

    def draw(self, surface):
        if self.health > 0:
            surface.blit(self.surf, self.rect)
        elif self.explosion and not self.explosion.finished:
            self.explosion.draw(surface)

    def is_finished(self):
        return self.health <= 0 and self.explosion is not None and self.explosion.finished
