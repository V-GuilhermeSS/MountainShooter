#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Module that defines the EntityFactory class.

EntityFactory provides a centralized way of creating game entities
such as backgrounds, players, and enemies. This avoids duplication
and ensures consistency in entity instantiation.
"""

import random
from Code.Background import Background
from Code.Const import WIN_WIDTH, WIN_HEIGHT
from Code.Enemy import Enemy
from Code.Player import Player


class EntityFactory:
    """
    Factory class responsible for creating instances of different entities.

    Methods:
        get_entity(entity_name, position):
            Creates and returns an entity instance or a list of entities
            depending on the type requested.
    """

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        """
        Create an entity instance based on the provided name.

        Args:
            entity_name (str): The name/type of the entity to create.
            position (tuple, optional): The (x, y) starting position of the entity.
                                        Defaults to (0, 0).

        Returns:
            list[Background] | Player | Enemy :
                - A list of Background objects (for levels).
                - A Player instance (Player1 or Player2).
                - An Enemy instance (Enemy1, Enemy2, Enemy3).
        """
        match entity_name:
            case 'Level1Bg':
                # Create 7 scrolling background layers for Level 1
                list_bg = []
                for i in range(7):
                    list_bg.append(Background(f'Level1Bg{i}', position))
                    list_bg.append(Background(f'Level1Bg{i}', (WIN_WIDTH, 0)))
                return list_bg

            case 'Level2Bg':
                # Create 5 scrolling background layers for Level 2
                list_bg = []
                for i in range(5):
                    list_bg.append(Background(f'Level2Bg{i}', position))
                    list_bg.append(Background(f'Level2Bg{i}', (WIN_WIDTH, 0)))
                return list_bg

            case 'Player1':
                # Spawn Player 1 on screen
                return Player('Player1', (10, WIN_HEIGHT / 2 - 30))

            case 'Player2':
                # Spawn Player 2 on screen
                return Player('Player2', (10, WIN_HEIGHT / 2 + 30))

            case 'Enemy1':
                # Spawn Enemy1 off-screen to the right, random vertical position
                return Enemy('Enemy1', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

            case 'Enemy2':
                # Spawn Enemy2 off-screen to the right, random vertical position
                return Enemy('Enemy2', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))

            case 'Enemy3':
                # Spawn Enemy3 off-screen to the right, random vertical position
                return Enemy('Enemy3', (WIN_WIDTH + 10, random.randint(40, WIN_HEIGHT - 40)))
