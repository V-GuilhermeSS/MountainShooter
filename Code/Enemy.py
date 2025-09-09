#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module responsible for implementing the Enemy class.

The Enemy class represents enemies in the game, inheriting from Entity.
Controls shooting, shots, explosions, and points awarded to the player.
"""
import random

import pygame

from Code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY, SHOT_SOUNDS, EXPLOSION_SOUND
from Code.EnemyShot import EnemyShot
from Code.Entity import Entity
from Code.Explosion import Explosion


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        """
            Initializes the enemy with specific attributes.

            Args:
            name (str): Enemy name (defines speed, sound, and rate of fire).
            position (tuple): Initial position (x, y) of the enemy on the screen.
        """
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]  # initial trigger interval
        self.explosion: Explosion | None = None
        self.score_given = False  # ensures that the score is added only once
        self.name = name
        # Sounds of gunfire and explosions associated with the enemy
        self.shoot_sound = pygame.mixer.Sound(SHOT_SOUNDS.get(self.name))
        self.explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND[self.name])

        self.has_shot_once = False  # prevent immediate firing after spawn
        self.shot_delay = 10  # initial delay before first shot
        self.active_shots = []  # enemy active fire list

    def move(self):
        """
        Updates the enemy's horizontal position.

        - If alive: Moves left based on the set speed.
        - If destroyed: Starts or updates the explosion animation.
        """
        if self.health > 0:
            # Enemy moves from right to left
            self.rect.centerx -= ENTITY_SPEED[self.name]
        else:
            # If the explosion hasn't started yet, play the sound and create the effect
            if not self.explosion:
                self.explosion_sound.play()
                self.explosion = Explosion(position=self.rect.center, scale=1.0, frame_delay=4, name=self.name)
            else:
                # Explosion animation continues
                self.explosion.update()

    def shoot(self):
        """
        Manages enemy shots.

        - Respects the firing delay set for each enemy type.
        - After the first shot, the delays vary between the maximum value
        and half of it, chosen randomly.

        Returns:
        EnemyShot | None: Instance of EnemyShot if the enemy fires,
        otherwise returns None.
        """
        if self.health <= 0:
            return None  # destroyed enemy cannot shoot

        self.shot_delay -= 1  # reduce the delay counter

        if self.shot_delay <= 0:
            if not self.has_shot_once:
                # First trigger occurs after initial delay
                self.has_shot_once = True
            else:
                # After the first shot, draw a new delay
                max_delay = ENTITY_SHOT_DELAY[self.name]
                self.shot_delay = random.choice([max_delay, max_delay // 2])

            # Plays the gunshot sound and creates the gunshot
            self.shoot_sound.play()
            pygame.mixer.Sound.set_volume(self.shoot_sound, 0.5)
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

        return None

    def draw(self, surface):
        """
        Draws the enemy or its explosion on the screen.

        Args:
        surface (pygame.Surface): Surface where it will be drawn.
        """
        if self.health > 0:
            surface.blit(self.surf, self.rect)  # draw the enemy alive
        elif self.explosion and not self.explosion.finished:
            self.explosion.draw(surface)  # draw enemy explosion

    def is_finished(self):
        """
        Checks whether the enemy has been completely destroyed.

        Returns:
        bool: True if the enemy is dead and the explosion has completed.
        """
        return self.health <= 0 and self.explosion is not None and self.explosion.finished
