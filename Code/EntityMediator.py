#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
EntityMediator module.
Provides static methods to manage collisions, health, and scoring
between different types of entities (Player, Enemy, Shots, etc.).
"""

from Code.Const import WIN_WIDTH
from Code.Enemy import Enemy
from Code.EnemyShot import EnemyShot
from Code.Entity import Entity
from Code.Player import Player
from Code.PlayerShot import PlayerShot


class EntityMediator:
    """
    Mediator class responsible for handling entity interactions:
    - Collision with window boundaries
    - Collision between entities
    - Scoring attribution
    - Health verification and entity removal
    """

    @staticmethod
    def __verify_collision_window(ent: Entity):
        """
        Check if an entity collides with the game window boundaries.
        Marks entity for removal if it goes out of bounds.

        :param ent: Entity instance to check
        """
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                # Enemy left the screen -> remove immediately, no explosion
                ent.to_remove = True
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                # Player's shot went off the right side -> remove
                ent.to_remove = True
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                # Enemy's shot went off the left side -> remove
                ent.to_remove = True

    @staticmethod
    def __verify_collision_entity(ent1: Entity, ent2: Entity):
        """
        Check collision between two entities and apply damage logic.

        :param ent1: First entity
        :param ent2: Second entity
        """
        valid_interaction = False

        # Define valid collision interactions
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
            # Check bounding box collision
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):

                # --- Special case: Player vs Enemy ---
                if isinstance(ent1, Player) and isinstance(ent2, Enemy):
                    if not getattr(ent2, 'collided_with_player', False):
                        ent1.health -= 100  # Player loses 100 HP
                        ent2.health = 0  # Enemy explodes
                        ent2.collided_with_player = True
                elif isinstance(ent2, Player) and isinstance(ent1, Enemy):
                    if not getattr(ent1, 'collided_with_player', False):
                        ent2.health -= 100
                        ent1.health = 0
                        ent1.collided_with_player = True
                else:
                    # Default collision behavior: apply mutual damage
                    ent1.health -= ent2.damage
                    ent2.health -= ent1.damage

                # Track last entity that inflicted damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        """
        Assign score to the player who defeated an enemy.
        Prevents score from being given more than once.

        :param enemy: Enemy instance that was destroyed
        :param entity_list: List of all active entities
        """
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
        """
        Check all entities for collisions (window and entity-to-entity).

        :param entity_list: List of all active entities
        """
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        """
        Remove entities with no health or marked for removal.
        Also handles scoring attribution and explosion lifecycles.

        :param entity_list: List of all active entities
        """
        for ent in entity_list[:]:
            # Case: removed directly (no explosion)
            if getattr(ent, "to_remove", False):
                try:
                    entity_list.remove(ent)
                except ValueError:
                    pass
                continue

            if ent.health <= 0:
                # Give score to player (if enemy), only once
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)

                # If entity has is_finished() -> wait until explosion is done
                if hasattr(ent, "is_finished"):
                    try:
                        if ent.is_finished():
                            entity_list.remove(ent)
                    except (ValueError, AttributeError):
                        # Fallback in case of explosion error
                        try:
                            entity_list.remove(ent)
                        except ValueError:
                            pass
                else:
                    # Default case: remove immediately
                    try:
                        entity_list.remove(ent)
                    except ValueError:
                        pass
