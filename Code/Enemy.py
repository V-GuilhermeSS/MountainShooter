#!/usr/bin/python
# -*- coding: utf-8 -*-
from Code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from Code.EnemyShot import EnemyShot
from Code.Entity import Entity
from Code.Explosion import Explosion


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.explosion: Explosion | None = None
        self.score_given = False  # garante que a pontuação seja somada apenas 1 vez

    def move(self):
        if self.health > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        else:
            if not self.explosion:
                self.explosion = Explosion(position=self.rect.center, scale=1.0, frame_delay=4)
            else:
                self.explosion.update()

    def shoot(self):
        if self.health <= 0:
            return None
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        return None

    def draw(self, surface):
        if self.health > 0:
            surface.blit(self.surf, self.rect)
        elif self.explosion and not self.explosion.finished:
            self.explosion.draw(surface)

    def is_finished(self):
        return self.health <= 0 and self.explosion is not None and self.explosion.finished
