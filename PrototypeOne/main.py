import pygame, pygame_gui
from src import Constants
from src.Game import Game
from src.Screens import ScreenType
from pygame_gui import UIManager

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
clock = pygame.time.Clock()
manager = UIManager((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
running: bool = True
deltaAccumulator: float = 0
game: Game = Game()
game.SwitchScreen(manager, ScreenType.MAIN_MENU)

while running:
    time_delta: float = clock.tick(Constants.FPS)/1000.0
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                game.KeyDown(event, time_delta)
        
        manager.process_events(event)

    if deltaAccumulator <= 0:
        deltaAccumulator = 1.0 / 60
        keys = pygame.key.get_pressed()

        game.AccumulatedInput(keys)
    else:
        deltaAccumulator -= time_delta

    game.Update(time_delta)

    manager.update(time_delta)

    screen.fill(Constants.FILL_COLOR)
    game.Render(screen)
    manager.draw_ui(screen)

    pygame.display.flip()