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
game: Game = Game(UIManager((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)))
game.SwitchScreen(manager, ScreenType.MAIN_MENU)

while running:
    time_delta: float = min(clock.tick(Constants.FPS)/1000.0, 1/Constants.FPS)
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                game.KeyDown(event, time_delta)
        
        manager.process_events(event)
        game.editor.manager.process_events(event)

    if deltaAccumulator <= 0:
        deltaAccumulator = 1.0 / 60
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        game.AccumulatedInput(keys, mouse)
    else:
        deltaAccumulator -= time_delta

    game.Update(manager, time_delta)

    manager.update(time_delta)
    game.editor.manager.update(time_delta)

    screen.fill(Constants.FILL_COLOR)
    game.Render(screen)
    manager.draw_ui(screen)
    game.editor.manager.draw_ui(screen)

    pygame.display.flip()