#!/usr/bin/python
# -*- coding: utf-8 -*-
# Import window width and entity speed mapping
from Code.Const import WIN_WIDTH, ENTITY_SPEED
# Import base class for all game entities
from Code.Entity import Entity

"""
    Module responsible for the background class, 
which represents the game's animated background.
    It inherits from Entity and implements continuous background movements, 
simulating an infinite scrolling effects.
"""


class Background(Entity):
    """
    A class that represents the game's animated background.

    The class inherits from Entity and implements continuous horizontal movement,
    repositioning the background when it moves off the screen to the left.
    This effect is called parallax.
    """
    def __init__(self, name: str, position: tuple):
        """
        Initializes a Background instance.

        Args:
        name (str): Background name, used to map velocity.
        position (tuple): Background starting position (x, y).
        """
        super().__init__(name, position)

    def move(self):
        """
        Updates the horizontal position of the background based on the defined speed.

        This method shifts the background to the left, simulating continuous movement.
        When the background completely extends beyond the left edge of the screen, it is repositioned
        on the right edge, creating an infinite scroll effect.

        Attributes used:
        - self.name: Name of the background type, used to find the corresponding speed.
        - self.rect: pygame.Rect object representing the position and dimensions of the background.
        - ENTITY_SPEED: Dictionary mapping entity names to their speeds.
        - WIN_WIDTH: Width of the game window, used to reposition the background.

        Does not return any value.
        """
        #  Apply horizontal translation based on predefined speed for this background type
        self.rect.centerx -= ENTITY_SPEED[self.name]
        #  If the background has fully exited the left side of the screen, reposition it to the right to create
        #  a seamless scrolling effect.
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
