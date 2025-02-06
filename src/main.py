#! /usr/bin/env python3
############## mazegame ###############
# 迷路のデータ構造
# 1 1 1 1 1
# 1 0 0 0 1
# 1 0 1 0 1
# 1 0 0 0 1
# 1 1 1 1 1
#
# 1 が壁で0が通路


# import
import pygame
import random
import time
from modules.MazeGame import MazeGame

# Paremeters
WIDTH, HEIGHT = 21, 21 # maze sizes
CELL_SIZE = 20 # cell size
DIRECTIONS = [(-2, 0), (2, 0), (0, -2), (0, 2)] # directions
SPEED = 15 # moving speed


# main class
class runMazeGame:
    """
    A class to run the MazeGame by handling game loop and events.
    """
    
    def __init__(self, mazegame: 'MazeGame') -> None:
        """
        Initialize the runMazeGame class with a MazeGame instance.

        Args:
            mazegame (MazeGame): An instance of the MazeGame class.
        """
        self.mazegame = mazegame

    def run(self) -> None:
        """
        Run the game loop, handling events and updating the game state.
        """
        running = True
        while running:
            self.mazegame.screen.fill(self.mazegame.color["black"])
            self.mazegame.draw_maze()
            self.mazegame.draw_player_and_goal()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            self.mazegame.move_player(keys)
            running = self.mazegame.check_goal()
            self.mazegame.clock.tick(self.mazegame.speed)
        pygame.quit()


if __name__ == "__main__":
    # module instanciation
    mazeGame = MazeGame(width=WIDTH, height=HEIGHT, cell_size=CELL_SIZE, speed=SPEED)
    game = runMazeGame(mazeGame)
    game.run()