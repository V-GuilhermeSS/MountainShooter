#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from Code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from Code.Entity import Entity
from Code.PlayerShot import PlayerShot
from Code.Explosion import Explosion


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.explosion: Explosion | None = None

    def move(self):
        if self.health > 0:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
                self.rect.centery -= ENTITY_SPEED[self.name]
            if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
                self.rect.centery += ENTITY_SPEED[self.name]
            if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
                self.rect.centerx -= ENTITY_SPEED[self.name]
            if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
                self.rect.centerx += ENTITY_SPEED[self.name]
        else:
            # Cria explosão assim que detecta morte (se ainda não criada)
            if not self.explosion:
                # ajuste frame_delay/scale se quiser
                self.explosion = Explosion(position=self.rect.center, scale=1.0, frame_delay=4)
            else:
                self.explosion.update()

    def shoot(self):
        if self.health <= 0:
            return None
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
            else:
                return None
        else:
            return None

    def draw(self, surface):
        if self.health > 0:
            surface.blit(self.surf, self.rect)
        elif self.explosion and not self.explosion.finished:
            self.explosion.draw(surface)

    def is_finished(self):
        """Indica se a entidade pode ser removida da lista (explosão terminou)."""
        return self.health <= 0 and self.explosion is not None and self.explosion.finished
