#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import pygame.display

from pygame import Surface, Rect
from pygame.font import Font
from Code.Const import (
    C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME,
    C_GREEN, C_CYAN, EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL, LEVEL_SCORE_THRESHOLD
)
from Code.Enemy import Enemy
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory
from Code.EntityMediator import EntityMediator
from Code.Player import Player


class Level:
    """
    Represents a game level. Handles entity spawning, player/enemy updates,
    scoring, timeout checks, and rendering text on the screen.
    """
    def __init__(self, window, name: str, game_mode: str, player_score: list[int]):
        """
        Initialize the Level instance.

        :param window: Pygame display surface
        :param name: Level name (used to load background and music)
        :param game_mode: Selected game mode
        :param player_score: Current player scores to be updated during gameplay
        """
        self.timeout = TIMEOUT_LEVEL  # Level duration in milliseconds
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Load background entities for the level
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))

        self.game_over = False
        self.game_over_time = None
        self.font_big = pygame.font.SysFont("Lucida Sans Typewriter", 72, bold=True)
        self.font_small = pygame.font.SysFont("Lucida Sans Typewriter", 28)

        # Explosion effect tracking when all players die
        self.explosion_triggered = False
        self.explosion_time = None

        # Add Player 1
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        # Add Player 2 if in multiplayer mode
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        # Setup timed events
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME[self.name])
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def run(self, player_score: list[int]):
        """
        Main loop of the level. Handles events, entity updates, collision checks,
        scoring, timeout, and rendering of game info.

        :param player_score: Current scores, updated during gameplay
        :return: Updated player scores and level status ("game_over" or "score_clear")
        """
        # Load and play background music
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        pygame.mixer_music.set_volume(0.3)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)  # Maintain 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.game_over:
                    # Spawn random enemy on timer
                    if event.type == EVENT_ENEMY:
                        choice = random.choice(('Enemy1', 'Enemy2', 'Enemy3'))
                        self.entity_list.append(EntityFactory.get_entity(choice))

                    # Reduce timeout
                    if event.type == EVENT_TIMEOUT:
                        self.timeout -= TIMEOUT_STEP

                        # Timeout reached -> game over
                        if self.timeout <= 0:
                            for ent in self.entity_list:
                                if isinstance(ent, Player) and ent.name == 'Player1':
                                    player_score[0] = ent.score
                                if isinstance(ent, Player) and ent.name == 'Player2':
                                    player_score[1] = ent.score
                            return player_score, "game_over"

                    # Check if any player reached score threshold -> level clear
                    if self.timeout > 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player):
                                if ent.name == 'Player1' and ent.score >= LEVEL_SCORE_THRESHOLD[self.name]:
                                    player_score[0] = ent.score
                                    return player_score, "score_clear"
                                if ent.name == 'Player2' and ent.score >= LEVEL_SCORE_THRESHOLD[self.name]:
                                    player_score[1] = ent.score
                                    return player_score, "score_clear"

            # If no players remain, trigger game over
            if not any(isinstance(ent, Player) for ent in self.entity_list):
                return player_score, "game_over"

            # Update and draw entities
            for ent in self.entity_list[:]:
                ent.move()

                # Entities capable of shooting generate shots
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                # Draw entity if it has a draw method, otherwise blit the sprite
                if hasattr(ent, "draw"):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

            # Render player HUD (Health and Score)
            for ent in self.entity_list:
                if ent.name == 'Player1':
                    self.level_text(14, f'Player1 - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
                if ent.name == 'Player2':
                    self.level_text(14, f'Player2 - Health: {ent.health} | Score: {ent.score}', C_CYAN, (10, 45))

            # Trigger explosion and game over when all players die
            if not any(isinstance(ent, Player) for ent in self.entity_list):
                if not self.explosion_triggered:
                    self.explosion_triggered = True
                    self.explosion_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - self.explosion_time > 4000:  # Wait 4 seconds before game over
                    self.game_over = True
                    self.game_over_time = pygame.time.get_ticks()

            # Render level info (timeout, FPS, entity count)
            self.level_text(14, f'{self.name} - Timeout {self.timeout / 1000:.1f}s', C_WHITE, (10, 1))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            # Collision and health management
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        """
        Render text on the game window.

        :param text_size: Font size
        :param text: Text to render
        :param text_color: RGB tuple
        :param text_pos: Position tuple (x, y)
        """
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
