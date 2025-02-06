import pygame
import random
import time
from types import SimpleNamespace

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 方向 (上下左右)
DIRECTIONS = [(-2, 0), (2, 0), (0, -2), (0, 2)]


class MazeGame:
    """
    A class representing a maze game using Pygame.
    """

    def __init__(self, width: int = 21, height: int = 21, cell_size: int = 20, speed: int = 15) -> None:
        """
        Initialize the MazeGame with given dimensions and speed.

        Args:
            width (int): The width of the maze.
            height (int): The height of the maze.
            cell_size (int): The size of each cell in pixels.
            speed (int): The speed of player movement.
        """
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.speed = speed
        self.color = {
            "red": RED,
            "blue": BLUE,
            "white": WHITE,
            "black": BLACK
        }
        self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        self.clock = pygame.time.Clock()
        self.font_congrats = pygame.font.Font(None, 30)
        self.font_time = pygame.font.Font(None, 20)
        self.maze = self.generate_maze()
        self.player_x, self.player_y = 1, 1
        self.goal_x, self.goal_y = self.width - 2, self.height - 2
        self.start_time = time.time()
    
    def generate_maze(self) -> list:
        """
        Generate a random maze using depth-first search algorithm.

        Returns:
            list: A 2D list representing the maze structure.
        """
        maze = [[1] * self.width for _ in range(self.height)]
        stack = [(1, 1)]
        maze[1][1] = 0
        
        while stack:
            x, y = stack[-1]
            random.shuffle(DIRECTIONS)
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and maze[nx][ny] == 1:
                    maze[nx][ny] = 0
                    maze[x + dx // 2][y + dy // 2] = 0
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()
        
        return maze
    
    def draw_maze(self) -> None:
        """
        Draw the maze grid on the screen.
        """
        for y in range(self.height):
            for x in range(self.width):
                color = self.color["white"] if self.maze[y][x] == 0 else self.color["black"]
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
    
    def draw_player_and_goal(self) -> None:
        """
        Draw the player and the goal on the maze.
        """
        pygame.draw.rect(self.screen, self.color["red"], (self.player_x * self.cell_size, self.player_y * self.cell_size, self.cell_size, self.cell_size))
        pygame.draw.rect(self.screen, self.color["blue"], (self.goal_x * self.cell_size, self.goal_y * self.cell_size, self.cell_size, self.cell_size))
    
    def check_goal(self) -> bool:
        """
        Check if the player has reached the goal. Display a message if the goal is reached.

        Returns:
            bool: False if the player has reached the goal, True otherwise.
        """
        if self.player_x == self.goal_x and self.player_y == self.goal_y:
            end_time = time.time()
            time_elapsed = end_time - self.start_time

            text_congrats = self.font_congrats.render("GOAL! CONGRATULATION!", True, self.color["black"])
            text_time = self.font_time.render(f"Your time is: {time_elapsed:.2f}s", True, self.color["black"])
            text_congrats_rect = text_congrats.get_rect(center=(self.width * self.cell_size // 2, self.height * self.cell_size // 2))
            text_time_rect = text_time.get_rect(center=(self.width * self.cell_size // 2, self.height * self.cell_size // 2 + 15))
            
            box_rect = text_congrats_rect.inflate(20, 40)
            pygame.draw.rect(self.screen, self.color["white"], box_rect, 0, border_radius=10)
            pygame.draw.rect(self.screen, self.color["red"], box_rect, 2, border_radius=10)

            self.screen.blit(text_congrats, text_congrats_rect)
            self.screen.blit(text_time, text_time_rect)

            pygame.display.flip()
            time.sleep(5)
            return False
        return True
    
    def move_player(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        Move the player based on the pressed key inputs.

        Args:
            keys (pygame.key.ScancodeWrapper): The key input states.
        """
        if keys[pygame.K_UP] and self.maze[self.player_y - 1][self.player_x] == 0:
            self.player_y -= 1
        if keys[pygame.K_DOWN] and self.maze[self.player_y + 1][self.player_x] == 0:
            self.player_y += 1
        if keys[pygame.K_LEFT] and self.maze[self.player_y][self.player_x - 1] == 0:
            self.player_x -= 1
        if keys[pygame.K_RIGHT] and self.maze[self.player_y][self.player_x + 1] == 0:
            self.player_x += 1
