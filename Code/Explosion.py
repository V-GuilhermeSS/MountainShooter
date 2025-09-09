#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame import Surface, Rect
from Code.Const import EXPLOSION_FRAMES
from Code.Entity import Entity


class Explosion(Entity):
    """
    Represents an explosion animation sequence triggered when an entity is destroyed.

    This class handles loading explosion frames, scaling them if necessary,
    and updating/drawing the animation frame by frame until it is finished.
    """

    def __init__(self, position: tuple, name: str, scale: float = 1.0, frame_delay: int = 4):
        """
        Initialize an Explosion object.

        Args:
            position (tuple): Center position (x, y) of the explosion.
            name (str): Entity name, used to retrieve the corresponding explosion frames.
            scale (float, optional): Scaling factor for explosion images. Defaults to 1.0.
            frame_delay (int, optional): Number of game frames each animation frame should last. Defaults to 4.

        Raises:
            ValueError: If no explosion frames are defined for the given entity name.
        """
        super().__init__(name, position)

        # Retrieve explosion frame file names from the dictionary
        frame_files = EXPLOSION_FRAMES.get(name, [])
        if not frame_files:
            raise ValueError(f"No explosion frames defined for {name}")

        # Load all explosion frames into memory
        self.frames = [pygame.image.load(f'./asset/{file}').convert_alpha() for file in frame_files]

        # Apply scaling if required
        if scale != 1.0:
            self.frames = [
                pygame.transform.scale(
                    f,
                    (int(f.get_width() * scale), int(f.get_height() * scale))
                )
                for f in self.frames
            ]

        # Current frame index
        self.index = 0
        # Position of the explosion (based on first frame)
        self.rect: Rect = self.frames[0].get_rect(center=position)
        # Flag to indicate if the animation is finished
        self.finished = False

        # Animation speed control
        self.frame_delay = max(1, frame_delay)  # Prevents invalid (<=0) delays
        self._delay_counter = 0

    def update(self):
        """
        Updates the explosion animation.

        This should be called once per game frame.
        Increments the delay counter and advances the animation
        to the next frame when the delay threshold is reached.
        """
        if self.finished:
            return

        self._delay_counter += 1
        if self._delay_counter >= self.frame_delay:
            self._delay_counter = 0
            if self.index < len(self.frames) - 1:
                self.index += 1
            else:
                self.finished = True  # Animation has completed

    def draw(self, surface: Surface):
        """
        Draws the current frame of the explosion onto the given surface.

        Args:
            surface (Surface): The pygame surface to render the explosion on.
        """
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)

    def move(self):
        """
        Explosion does not move across the screen.

        This method is defined to maintain consistency with the Entity interface.
        """
        pass
