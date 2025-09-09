#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION, C_YELLOW, C_WHITE
from Code.Level import Level
from Code.Menu import Menu
from Code.Score import Score


class Game:
    """
    Main game controller class.

    Handles initialization, main loop, menu navigation, level progression,
    and Game Over screen display with fade-in/fade-out effects.
    """

    def __init__(self):
        """Initialize pygame and create the game window."""
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        """
        Main game loop.

        - Shows menu and responds to selection
        - Handles level progression (Level1 -> Level2)
        - Shows score or exits game based on menu selection
        """
        while True:
            # Initialize score manager
            score = Score(self.window)
            # Initialize menu
            menu = Menu(self.window)
            menu_return = menu.run()

            # --- Start new game ---
            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                game_over = False
                player_score = [0, 0]

                # Run Level 1
                level = Level(self.window, 'Level1', menu_return, player_score)
                player_score, level_status = level.run(player_score)

                # If cleared, run Level 2
                if level_status in ["score_clear"]:
                    level = Level(self.window, 'Level2', menu_return, player_score)
                    player_score, level_status = level.run(player_score)

                    # Save score if cleared Level 2
                    if level_status in ["score_clear"]:
                        score.save(menu_return, player_score)
                    else:
                        game_over = True
                else:
                    game_over = True

                if game_over:
                    self.show_game_over()

            # --- Show score table ---
            elif menu_return == MENU_OPTION[3]:
                score.show()

            # --- Exit game ---
            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()

    def show_game_over(self):
        """
        Display Game Over screen with fade-in and fade-out effects.

        - Shows "GAME OVER" text
        - Displays countdown before returning to menu
        - Handles smooth transition using fade-in and fade-out overlays
        """
        font_big = pygame.font.SysFont("Lucida Sans Typewriter", 72, bold=True)
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 28)

        clock = pygame.time.Clock()
        pygame.time.delay(2000)  # Initial delay before starting fade

        start_time = pygame.time.get_ticks()
        fade_in_duration = 3000  # Duration of fade-in
        total_duration = 8000    # Total display time
        fade_out_duration = 2000  # Duration of fade-out

        while True:
            elapsed = pygame.time.get_ticks() - start_time
            remaining = max(0, (total_duration - elapsed) // 1000)

            # --- Fade-in overlay ---
            alpha = int((elapsed / fade_in_duration) * 150) if elapsed < fade_in_duration else 150
            overlay = pygame.Surface(self.window.get_size())
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            # --- Display texts after fade-in ---
            if elapsed >= fade_in_duration:
                text = font_big.render("GAME OVER", True, C_YELLOW)
                text_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 40))
                self.window.blit(text, text_rect)

                press_esc = font_small.render(f"Back to Menu in {remaining}s...", True, C_WHITE)
                press_esc_rect = press_esc.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 40))
                self.window.blit(press_esc, press_esc_rect)

            pygame.display.flip()
            clock.tick(60)
            pygame.time.delay(100)

            # End of total duration -> break to fade-out
            if elapsed >= total_duration:
                break

        # --- Fade-out to transition smoothly back to menu ---
        fade_out_steps = 30
        for i in range(fade_out_steps):
            alpha = int((i / fade_out_steps) * 255)
            overlay = pygame.Surface(self.window.get_size())
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.delay(fade_out_duration // fade_out_steps)
