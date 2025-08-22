#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC


from Code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from Code.Entity import Entity


class EnemyShot(Entity, ABC):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self, ):
        self.rect.centerx -= ENTITY_SPEED[self.name]


