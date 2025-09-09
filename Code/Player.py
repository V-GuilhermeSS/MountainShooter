#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key
from Code.Const import (
    ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN,
    PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY,
    SHOT_SOUNDS, EXPLOSION_SOUND
)
from Code.Entity import Entity
from Code.Explosion import Explosion
from Code.PlayerShot import PlayerShot


class Player(Entity):
    """
    Represents a player in the game. Inherits from Entity and adds:
    - Keyboard control for movement
    - Shooting mechanic with cooldown
    - Explosion effect upon death
    """

    def __init__(self, name: str, position: tuple):
        """
        Initialize the player.

        :param name: Player name (e.g., 'Player1' or 'Player2')
        :param position: Initial position as a tuple (x, y)
        """
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.explosion: Explosion | None = None
        self.shot_sound = pygame.mixer.Sound(SHOT_SOUNDS.get(self.name))
        self.last_shot_time = 0
        self.shot_cooldown = ENTITY_SHOT_DELAY[self.name]  # in milliseconds
        self.explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND[self.name])

    def move(self):
        """
        Update the player's position based on keyboard input.
        If the player is dead, trigger or update the explosion effect.
        """
        if self.health > 0:
            pressed_key = pygame.key.get_pressed()
            # Vertical movement
            if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
                self.rect.centery -= ENTITY_SPEED[self.name]
            if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
                self.rect.centery += ENTITY_SPEED[self.name]
            # Horizontal movement
            if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
                self.rect.centerx -= ENTITY_SPEED[self.name]
            if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
                self.rect.centerx += ENTITY_SPEED[self.name]
        else:
            # Create an explosion when player dies (if not already created)
            if not self.explosion:
                self.explosion_sound.play()
                self.explosion = Explosion(
                    position=self.rect.center,
                    scale=1.0,
                    frame_delay=4,
                    name=self.name
                )
            else:
                # Update the explosion animation
                self.explosion.update()

    def shoot(self):
        """
        Attempt to shoot a projectile if the shoot key is pressed
        and the cooldown period has passed.

        :return: PlayerShot object if fired, None otherwise
        """
        if self.health <= 0:
            return None

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                self.last_shot_time = current_time
                self.shot_sound.play()
                pygame.mixer.Sound.set_volume(self.shot_sound, 0.5)
                return PlayerShot(
                    name=f'{self.name}Shot',
                    position=(self.rect.centerx, self.rect.centery)
                )
        return None

    def draw(self, surface: pygame.Surface):
        """
        Draw the player on the given surface.
        If the player is dead, draw the explosion instead.

        :param surface: Pygame surface to draw on
        """
        if self.health > 0:
            surface.blit(self.surf, self.rect)
        elif self.explosion and not self.explosion.finished:
            self.explosion.draw(surface)

    def is_finished(self) -> bool:
        """
        Check if the entity can be safely removed from the entity list.
        This occurs when the player is dead and the explosion animation is finished.

        :return: True if the player and explosion are finished, False otherwise
        """
        return self.health <= 0 and self.explosion is not None and self.explosion.finished
