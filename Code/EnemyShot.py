#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module that defines the EnemyShot class.

The EnemyShot class represents projectiles fired by enemies,
inheriting the basic structure from Entity.
"""

from abc import ABC
from Code.Const import ENTITY_SPEED
from Code.Entity import Entity


class EnemyShot(Entity, ABC):
    """
    Class representing an enemy projectile in the game.

    Inherits from Entity and implements only horizontal movement.
    """

    def __init__(self, name: str, position: tuple):
        """
        Initialize an enemy shot.

        Args:
            name (str): Identifier for the type of shot (used in speed mapping).
            position (tuple): Initial position (x, y) of the shot on the screen.
        """
        super().__init__(name, position)

    def move(self):
        """
        Update the horizontal position of the enemy shot.

        The shot moves from right to left across the screen
        according to the predefined speed in ENTITY_SPEED.
        """
        # Move the shot horizontally to the left
        self.rect.centerx -= ENTITY_SPEED[self.name]
