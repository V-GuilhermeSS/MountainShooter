#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC
from Code.Const import ENTITY_SPEED
from Code.Entity import Entity


class PlayerShot(Entity, ABC):
    """
    Represents a projectile shot by a player.
    Inherits from Entity and provides simple horizontal movement.
    """

    def __init__(self, name: str, position: tuple):
        """
        Initialize the player shot.

        :param name: Name of the shot (e.g., 'Player1Shot')
        :param position: Initial position as a tuple (x, y)
        """
        super().__init__(name, position)

    def move(self):
        """
        Move the shot horizontally across the screen.
        The speed is defined by ENTITY_SPEED for the shot's name.
        """
        self.rect.centerx += ENTITY_SPEED[self.name]
