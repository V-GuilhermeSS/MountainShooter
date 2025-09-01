#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame import Surface, Rect

from Code.Const import EXPLOSION_FRAMES
from Code.Entity import Entity


class Explosion(Entity):
    def __init__(self, position: tuple, name: str, scale: float = 1.0, frame_delay: int = 4):
        """
        Position: centro da explosão (x, y)
        name: nome da entidade (para buscar os frames no dicionário)
        scale: fator de escala das imagens
        frame_delay: quantos frames do jogo cada frame da animação deve durar
        """

        super().__init__(name, position)

        # pega os frames da explosão a partir do dicionário
        frame_files = EXPLOSION_FRAMES.get(name, [])
        if not frame_files:
            raise ValueError(f"Nenhum frame de explosão definido para {name}")

        self.frames = [pygame.image.load(f'./asset/{file}').convert_alpha() for file in frame_files]

        # aplica escala se necessário
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

    def move(self):
        pass
