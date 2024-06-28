import pygame
import sys
from game import TicTacToeGame
from ui import UI

pygame.init()

def main():
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Jogo da Velha")
    clock = pygame.time.Clock()
    
    game = TicTacToeGame()
    ui = UI(screen, game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            ui.handle_event(event)

        ui.update()
        ui.draw()
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
