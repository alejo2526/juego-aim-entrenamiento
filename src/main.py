import pygame
from game import Game
from app.constants import *

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game = Game()
    
    while True:
        if game.game_state == "enter_name":
            game.enter_name()
        elif game.game_state == "menu":
            game.show_menu()
        elif game.game_state == "playing":
            game.run()
        elif game.game_state == "game_over":
            game.show_game_over()

if __name__ == "__main__":
    main()

