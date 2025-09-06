import pygame

# C

C_ORANGE = (245, 70, 15)  # Title of game
C_WHITE = (248, 248, 255)  # Menu option deselected
C_YELLOW = (255, 215, 0)  # Menu option selected / YOU WIN /
C_GREEN = (0, 128, 0)  # HUD
C_CYAN = (0, 128, 128)  # HUD player2

# E

EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
ENTITY_SPEED = {
    'Level1Bg0': 0,
    'Level1Bg1': 1,
    'Level1Bg2': 2,
    'Level1Bg3': 3,
    'Level1Bg4': 4,
    'Level1Bg5': 5,
    'Level1Bg6': 6,
    'Level2Bg0': 0,
    'Level2Bg1': 1,
    'Level2Bg2': 2,
    'Level2Bg3': 3,
    'Level2Bg4': 4,
    'Player1': 3,
    'Player1Shot': 2,
    'Player2': 3,
    'Player2Shot': 4,
    'Enemy1': 2,
    'Enemy1Shot': 5,
    'Enemy2': 1,
    'Enemy2Shot': 2,
    'Enemy3': 0.7,
    'Enemy3Shot': 2,
    'Explosion': 0
}

ENTITY_HEALTH = {
    'Level1Bg0': 999,
    'Level1Bg1': 999,
    'Level1Bg2': 999,
    'Level1Bg3': 999,
    'Level1Bg4': 999,
    'Level1Bg5': 999,
    'Level1Bg6': 999,
    'Level2Bg0': 999,
    'Level2Bg1': 999,
    'Level2Bg2': 999,
    'Level2Bg3': 999,
    'Level2Bg4': 999,
    'Player1': 300,
    'Player1Shot': 1,
    'Player2': 300,
    'Player2Shot': 1,
    'Enemy1': 50,
    'Enemy1Shot': 1,
    'Enemy2': 60,
    'Enemy2Shot': 1,
    'Enemy3': 750,
    'Enemy3Shot': 1,
    'Explosion': 1
}

ENTITY_SHOT_DELAY = {
    'Player1': 150,
    'Player2': 120,
    'Enemy1': 120,
    'Enemy2': 200,
    'Enemy3': 300
}

ENTITY_DAMAGE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Player1': 1,
    'Player1Shot': 25,
    'Player2': 1,
    'Player2Shot': 20,
    'Enemy1': 1,
    'Enemy1Shot': 20,
    'Enemy2': 1,
    'Enemy2Shot': 15,
    'Enemy3': 1,
    'Enemy3Shot': 100,
    'Explosion': 0
}

ENTITY_SCORE = {
    'Level1Bg0': 0,
    'Level1Bg1': 0,
    'Level1Bg2': 0,
    'Level1Bg3': 0,
    'Level1Bg4': 0,
    'Level1Bg5': 0,
    'Level1Bg6': 0,
    'Level2Bg0': 0,
    'Level2Bg1': 0,
    'Level2Bg2': 0,
    'Level2Bg3': 0,
    'Level2Bg4': 0,
    'Player1': 0,
    'Player1Shot': 0,
    'Player2': 0,
    'Player2Shot': 0,
    'Enemy1': 100,
    'Enemy1Shot': 0,
    'Enemy2': 125,
    'Enemy2Shot': 0,
    'Enemy3': 200,
    'Enemy3Shot': 0,
    'Explosion': 0
}

EXPLOSION_SOUND = {'Player1': './asset/8bit_bomb_explosion.wav',
                   'Player2': './asset/8bit_bomb_explosion.wav',
                   'Enemy1': './asset/8bit_bomb_explosion.wav',
                   'Enemy2': './asset/8bit_bomb_explosion.wav',
                   'Enemy3': './asset/8bit_bomb_explosion.wav'
                   }

EXPLOSION_FRAMES = {'Player1': [
    'Ship1_Explosion_001.png',
    'Ship1_Explosion_001.png',
    "Ship1_Explosion_008.png",
    "Ship1_Explosion_009.png",
    "Ship1_Explosion_012.png",
    "Ship1_Explosion_013.png",
    "Ship1_Explosion_014.png",
    "Ship1_Explosion_017.png",
    "Ship1_Explosion_019.png",
    "Ship1_Explosion_020.png"
],
    'Player2': [
        "Ship2_Explosion_000.png",
        "Ship2_Explosion_004.png",
        "Ship2_Explosion_005.png",
        "Ship2_Explosion_008.png",
        "Ship2_Explosion_009.png",
        "Ship2_Explosion_010.png",
        "Ship2_Explosion_013.png",
        "Ship2_Explosion_014.png",
        "Ship2_Explosion_015.png",
        "Ship2_Explosion_016.png",
        "Ship2_Explosion_019.png",
        "Ship2_Explosion_021.png"
    ], 'Enemy1': [
        "Ship3_Explosion_000.png",
        "Ship3_Explosion_004.png",
        "Ship3_Explosion_005.png",
        "Ship3_Explosion_007.png",
        "Ship3_Explosion_009.png",
        "Ship3_Explosion_012.png",
        "Ship3_Explosion_013.png",
        "Ship3_Explosion_015.png",
        "Ship3_Explosion_018.png",
        "Ship3_Explosion_019.png",
        "Ship3_Explosion_021.png"
    ],
    'Enemy2': [
        "Ship4_Explosion_000.png",
        "Ship4_Explosion_003.png",
        "Ship4_Explosion_005.png",
        "Ship4_Explosion_007.png",
        "Ship4_Explosion_008.png",
        "Ship4_Explosion_012.png",
        "Ship4_Explosion_013.png",
        "Ship4_Explosion_015.png",
        "Ship4_Explosion_018.png",
        "Ship4_Explosion_019.png",
        "Ship4_Explosion_020.png"
    ],
    'Enemy3': [
        "Ship6_Explosion_000.png",
        "Ship6_Explosion_004.png",
        "Ship6_Explosion_005.png",
        "Ship6_Explosion_007.png",
        "Ship6_Explosion_009.png",
        "Ship6_Explosion_011.png",
        "Ship6_Explosion_013.png",
        "Ship6_Explosion_016.png",
        "Ship6_Explosion_017.png",
        "Ship6_Explosion_019.png",
        "Ship6_Explosion_021.png"
    ]
}

# L

LEVEL_SCORE_THRESHOLD = {'Level1': 1000,
                         'Level2': 3000}

# M
MENU_OPTION = ('NEW GAME 1P',
               'NEW GAME 2P - COOPERATIVE',
               'NEW GAME 2P - COMPETITIVE',
               'SCORE',
               'EXIT')
# P
PLAYER_KEY_UP = {'Player1': pygame.K_UP,
                 'Player2': pygame.K_w}
PLAYER_KEY_DOWN = {'Player1': pygame.K_DOWN,
                   'Player2': pygame.K_s}
PLAYER_KEY_LEFT = {'Player1': pygame.K_LEFT,
                   'Player2': pygame.K_a}
PLAYER_KEY_RIGHT = {'Player1': pygame.K_RIGHT,
                    'Player2': pygame.K_d}
PLAYER_KEY_SHOOT = {'Player1': pygame.K_RCTRL,
                    'Player2': pygame.K_LCTRL}
# S
SPAWN_TIME = {'Level1': 4000,
              'Level2': 3000}

SHOT_SOUNDS = {
    'Player1': './asset/Fire_1.mp3',
    'Player2': './asset/Fire_4.mp3',
    'Enemy1': './asset/Fire_2.mp3',
    'Enemy2': './asset/Fire_5.mp3',
    'Enemy3': './asset/Fire_6.mp3'
}

# T
TIMEOUT_STEP = 100  # 100 miliseconds
TIMEOUT_LEVEL = 60000  # 20 seconds

# W
WIN_WIDTH = 576
WIN_HEIGHT = 324

# S
SCORE_POS = {
    'Title': (WIN_WIDTH / 2, 50),
    'EnterName': (WIN_WIDTH / 2, 80),
    'Label': (WIN_WIDTH / 2, 90),
    'Name': (WIN_WIDTH / 2, 110),
    0: (WIN_WIDTH / 2, 110),
    1: (WIN_WIDTH / 2, 130),
    2: (WIN_WIDTH / 2, 150),
    3: (WIN_WIDTH / 2, 170),
    4: (WIN_WIDTH / 2, 190),
    5: (WIN_WIDTH / 2, 210),
    6: (WIN_WIDTH / 2, 230),
    7: (WIN_WIDTH / 2, 250),
    8: (WIN_WIDTH / 2, 270),
    9: (WIN_WIDTH / 2, 300)
}
