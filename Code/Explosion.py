#!/usr/bin/python
# -*- coding: utf-8 -*-
from typing import List

import pygame
from pygame import Surface, Rect


class Explosion:
    def __init__(self, position: tuple, scale: float = 1.0, frame_delay: int = 4):
        """
        position: centro da explosão (x, y)
        scale: fator de escala das imagens
        frame_delay: quantos frames do jogo cada frame da animação deve durar
        """
        image_names: List[str] = [
            "Ship1_Explosion_001.png",
            "Ship1_Explosion_003.png",
            "Ship1_Explosion_008.png",
            "Ship1_Explosion_009.png",
            "Ship1_Explosion_012.png",
            "Ship1_Explosion_013.png",
            "Ship1_Explosion_017.png",
            "Ship1_Explosion_019.png",
            "Ship1_Explosion_020.png"
        ]

        self.frames = [pygame.image.load(f'./asset/{name}').convert_alpha() for name in image_names]

        if scale != 1.0:
            self.frames = [
                pygame.transform.scale(f, (int(f.get_width() * scale), int(f.get_height() * scale)))
                for f in self.frames
            ]

        self.index = 0
        self.rect: Rect = self.frames[0].get_rect(center=position)
        self.finished = False

        # controle de velocidade da animação
        self.frame_delay = max(1, frame_delay)
        self._delay_counter = 0

    def update(self):
        """Chamar a cada frame; controla avanço com frame_delay."""
        if self.finished:
            return
        self._delay_counter += 1
        if self._delay_counter >= self.frame_delay:
            self._delay_counter = 0
            if self.index < len(self.frames) - 1:
                self.index += 1
            else:
                self.finished = True

    def draw(self, surface: Surface):
        """Desenha o frame atual."""
        if not self.finished:
            surface.blit(self.frames[self.index], self.rect)
