#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from Code.Const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW


class Menu:
    """
    Represents the main game menu. Handles menu rendering, keyboard navigation,
    fade-in/fade-out transitions, and music playback.
    """

    def __init__(self, window):
        """
        Initialize the menu.

        :param window: Pygame display surface
        """
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def fade_in(self, duration=2000):
        """
        Fade-in transition effect when menu appears.

        :param duration: Duration of the fade-in in milliseconds
        """
        clock = pygame.time.Clock()
        steps = 30
        for i in range(steps):
            alpha = 255 - int((i / steps) * 255)

            # Draw menu background and menu texts
            self.window.blit(self.surf, self.rect)
            self.menu_text(50, 'Mountain', C_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(50, 'Shooter', C_ORANGE, (WIN_WIDTH / 2, 120))
            for j, option in enumerate(MENU_OPTION):
                self.menu_text(20, option, C_WHITE, (WIN_WIDTH / 2, 200 + 25 * j))

            # Overlay darkening effect
            overlay = pygame.Surface(self.window.get_size())
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            pygame.display.flip()
            clock.tick(2000 // duration * steps)

    def fade_out(self, duration=1000):
        """
        Fade-out transition effect when menu closes.

        :param duration: Duration of the fade-out in milliseconds
        """
        clock = pygame.time.Clock()
        steps = 30
        for i in range(steps):
            alpha = int((i / steps) * 255)

            # Draw menu background and menu texts
            self.window.blit(self.surf, self.rect)
            self.menu_text(50, 'Mountain', C_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(50, 'Shooter', C_ORANGE, (WIN_WIDTH / 2, 120))
            for j, option in enumerate(MENU_OPTION):
                self.menu_text(20, option, C_WHITE, (WIN_WIDTH / 2, 200 + 25 * j))

            # Overlay darkening effect
            overlay = pygame.Surface(self.window.get_size())
            overlay.set_alpha(alpha)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))

            pygame.display.flip()
            clock.tick(1000 // duration * steps)

    def run(self):
        """
        Main loop of the menu. Handles input, selection, and music playback.

        :return: Selected menu option as a string
        """
        menu_option = 0

        # Load and play menu music
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)
        pygame.mixer_music.set_volume(0.3)

        # Enable continuous key navigation while holding down keys
        pygame.key.set_repeat(300, 100)

        self.fade_in()

        while True:
            # Draw menu background and all menu options
            self.window.blit(self.surf, self.rect)
            self.menu_text(50, 'Mountain', C_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(50, 'Shooter', C_ORANGE, (WIN_WIDTH / 2, 120))

            for i, option in enumerate(MENU_OPTION):
                color = C_YELLOW if i == menu_option else C_WHITE
                self.menu_text(20, option, color, (WIN_WIDTH / 2, 200 + 25 * i))

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # Navigate down
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    # Navigate up
                    if event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)
                    # Confirm selection
                    if event.key == pygame.K_RETURN:
                        self.fade_out()
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """
        Render centered menu text on the screen.

        :param text_size: Font size
        :param text: Text to display
        :param text_color: RGB color tuple
        :param text_center_pos: Position to center the text (x, y)
        """
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
