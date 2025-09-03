#!/usr/bin/python
# -*- coding: utf-8 -*-
from Code.Const import WIN_WIDTH
from Code.Enemy import Enemy
from Code.EnemyShot import EnemyShot
from Code.Entity import Entity
from Code.Player import Player
from Code.PlayerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                # Remove direto, sem explosão
                ent.to_remove = True
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.to_remove = True
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.to_remove = True

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Enemy) and isinstance(ent2, Player):
            valid_interaction = True

        if valid_interaction:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                # --- Ajuste especial para Player x Enemy ---
                if isinstance(ent1, Player) and isinstance(ent2, Enemy):
                    if not getattr(ent2, 'collided_with_player', False):
                        ent1.health -= 100  # Player perde 40 HP
                        ent2.health = 0  # Enemy explode
                        ent2.collided_with_player = True
                elif isinstance(ent2, Player) and isinstance(ent1, Enemy):
                    if not getattr(ent1, 'collided_with_player', False):
                        ent2.health -= 40
                        ent1.health = 0
                        ent1.collided_with_player = True
                else:
                    # comportamento padrão
                    ent1.health -= ent2.damage
                    ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        # só dá a pontuação 1 vez
        if getattr(enemy, "score_given", False):
            return
        enemy.score_given = True

        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list[:]:
            # caso especial: removidos sem explosão
            if getattr(ent, "to_remove", False):
                try:
                    entity_list.remove(ent)
                except ValueError:
                    pass
                continue

            if ent.health <= 0:
                # atribui pontuação (se for inimigo) apenas 1 vez
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)

                # se tiver método is_finished -> só remove quando explosão acabar
                if hasattr(ent, "is_finished"):
                    try:
                        if ent.is_finished():
                            entity_list.remove(ent)
                    except Exception:
                        try:
                            entity_list.remove(ent)
                        except ValueError:
                            pass
                else:
                    try:
                        entity_list.remove(ent)
                    except ValueError:
                        pass
