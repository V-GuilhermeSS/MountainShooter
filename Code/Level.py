#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import sys
import pygame.display
from pygame import Surface, Rect
from pygame.font import Font

from Code.Const import (
    C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME,
    C_GREEN, C_CYAN, EVENT_TIMEOUT, TIMEOUT_STEP, TIMEOUT_LEVEL, C_YELLOW
)
from Code.Enemy import Enemy
from Code.EntityMediator import EntityMediator
from Code.Entity import Entity
from Code.EntityFactory import EntityFactory
from Code.Player import Player


class Level:
    def __init__(self, window, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        self.game_over = False
        self.game_over_time = None  # momento que entrou em game over

        # Fonte personalizada (Viper.ttf)
        self.font_big = pygame.font.SysFont("Lucida Sans Typewriter", 72, bold=True)
        self.font_small = pygame.font.SysFont("Lucida Sans Typewriter", 28)

        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # 100ms

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        pygame.mixer_music.set_volume(0.3)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.game_over:  # só gera inimigos se não está em game over
                    if event.type == EVENT_ENEMY:
                        choice = random.choice(('Enemy1', 'Enemy2'))
                        self.entity_list.append(EntityFactory.get_entity(choice))
                    if event.type == EVENT_TIMEOUT:
                        self.timeout -= TIMEOUT_STEP
                        if self.timeout == 0:
                            for ent in self.entity_list:
                                if isinstance(ent, Player) and ent.name == 'Player1':
                                    player_score[0] = ent.score
                                if isinstance(ent, Player) and ent.name == 'Player2':
                                    player_score[1] = ent.score
                            return True

            # --- GAME OVER ---
            if self.game_over:
                # tempo decorrido desde o Game Over
                elapsed = pygame.time.get_ticks() - self.game_over_time
                remaining = max(0, 5 - elapsed // 1000)

                # escurece tela (parcial)
                overlay = pygame.Surface(self.window.get_size())
                overlay.set_alpha(5)
                overlay.fill((100, 100, 100))
                self.window.blit(overlay, (0, 0))

                # texto Game Over
                text = self.font_big.render("GAME OVER", True, C_YELLOW)
                text_rect = text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2 - 40))
                self.window.blit(text, text_rect)

                # instrução com contador
                press_esc = self.font_small.render(f"Voltando ao Menu em {remaining}s...",
                                                   True, C_WHITE)
                press_esc_rect = press_esc.get_rect(center=(self.window.get_width() // 2,
                                                            self.window.get_height() // 2 + 40))
                self.window.blit(press_esc, press_esc_rect)

                pygame.display.flip()

                # após 5 segundos → volta ao Menu
                if elapsed > 5000:
                    return False
                continue  # não executa update normal
            # -----------------

            # Update + Draw normal
            for ent in self.entity_list[:]:
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                if hasattr(ent, "draw"):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

            # HUD
            for ent in self.entity_list:
                if ent.name == 'Player1':
                    self.level_text(14, f'Player1 - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
                if ent.name == 'Player2':
                    self.level_text(14, f'Player2 - Health: {ent.health} | Score: {ent.score}', C_CYAN, (10, 45))

            # Se não há players → ativa game over
            if not any(isinstance(ent, Player) for ent in self.entity_list):
                self.game_over = True
                self.game_over_time = pygame.time.get_ticks()

            # HUD extra
            self.level_text(14, f'{self.name} - Timeout {self.timeout / 1000:.1f}s', C_WHITE, (10, 1))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
            pygame.display.flip()

            # Collisions
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
