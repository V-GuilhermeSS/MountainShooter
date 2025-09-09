#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module that defines the abstract Entity class.

The Entity class serves as a base for all game entities (players,
enemies, shots, backgrounds, etc.), providing common attributes
such as health, damage, score, and sprite handling.
"""

from abc import ABC, abstractmethod
import pygame.image
from Code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):
    """
    Abstract base class for all entities in the game.

    Attributes:
        name (str): Identifier of the entity, also used to load its sprite.
        surf (Surface): Sprite image of the entity.
        rect (Rect): Rectangle defining the position and dimensions of the entity.
        speed (int/float): Movement speed of the entity.
        health (int): Health points of the entity.
        damage (int): Damage dealt by the entity when colliding or attacking.
        score (int): Score awarded when the entity is destroyed.
        last_dmg (str): Name of the last source that damaged this entity.
    """

    def __init__(self, name: str, position: tuple):
        """
        Initialize a new entity with basic attributes.

        Args:
            name (str): Entity identifier, must match an asset image name.
            position (tuple): Initial position (x, y) of the entity.
        """
        self.name = name
        # Load the sprite from assets based on the entity name
        self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()
        # Define the position of the sprite on screen
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        # Default attributes from constants
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'

    @abstractmethod
    def move(self):
        """
        Abstract method for entity movement.

        Must be implemented by subclasses to define
        how the entity moves across the screen.
        """
        pass
