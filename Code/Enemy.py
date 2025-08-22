#!/usr/bin/python
# -*- coding: utf-8 -*-
from Code.Const import ENTITY_SPEED, WIN_WIDTH
from Code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, ):
        self.rect.centerx -= ENTITY_SPEED[self.name]
