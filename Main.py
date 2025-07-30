import pygame

pygame.init()
print('setup Start')

window = pygame.display.set_mode(size=(600, 480))
print('Setup End')

print('Loop Start')
while True:
    # Check all envents
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Close Window
            print('End...')
            quit()  # End pygame
