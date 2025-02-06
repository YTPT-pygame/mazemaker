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


import pygame
import random
import time

# 迷路のサイズ
WIDTH, HEIGHT = 21, 21  # 奇数にする
CELL_SIZE = 20

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 方向 (上下左右)
DIRECTIONS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# キャラクターconfig
player_x, player_y = 1, 1 # プレイヤーの初期位置
SPEED = 15 # 移動速度

# ゴール
GOAL_X, GOAL_Y = CELL_SIZE - 1, CELL_SIZE - 1 # ゴール位置

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0
    
    while stack:
        x, y = stack[-1]
        random.shuffle(DIRECTIONS)
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 1 <= nx < height-1 and 1 <= ny < width-1 and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + dx//2][y + dy//2] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
    
    return maze

# ゲームの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
clock = pygame.time.Clock()
maze = generate_maze(WIDTH, HEIGHT)
font_congrats = pygame.font.Font(None, 30)
font_time = pygame.font.Font(None, 20)


def draw_maze():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


### loop
running = True
start_time = time.time()
while running:
    screen.fill(BLACK)
    draw_maze()
    pygame.draw.rect(screen, RED, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # player描画 
    pygame.draw.rect(screen, BLUE, (GOAL_X * CELL_SIZE, GOAL_Y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) # goal描画

    #  playerのgoal時
    if player_x == GOAL_X and player_y == GOAL_Y:
        # 時間の計測
        end_time = time.time()
        time_elapsed = end_time - start_time

        # テキストを作成
        text_congrats = font_congrats.render("GOAL! CONGRATULATION!", True, BLACK)
        text_congrats_rect = text_congrats.get_rect(center=( (WIDTH // 2) * CELL_SIZE, (HEIGHT // 2) * CELL_SIZE))  # 画面中央に配置
        text_time = font_time.render(f"Your time is: {time_elapsed:.2f}s", True, BLACK)
        text_time_rect = text_time.get_rect(center=( (WIDTH // 2) * CELL_SIZE, (HEIGHT // 2) * CELL_SIZE + 15))  # 画面中央下部に配置


        # ボックス（枠）を描画
        padding = 20  # ボックスの余白
        box_rect = text_congrats_rect.inflate(padding, padding+padding)  # テキストのサイズを広げる
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 0, border_radius=10)  # 白い枠、角を丸める、塗りつぶし
        pygame.draw.rect(screen, RED, box_rect, 2, border_radius=10)  # 赤いフチ
 
         # テキストを描画
        screen.blit(text_congrats, text_congrats_rect)
        screen.blit(text_time, text_time_rect)

        # 更新
        pygame.display.flip()
        time.sleep(5)

        running = False # goalで終了

    pygame.display.flip()

    # もし画面が閉じられたら終了
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # キーの状態を取得
    keys = pygame.key.get_pressed()
    
    # 移動処理（押し続けると移動し続ける）
    if keys[pygame.K_UP] and maze[player_y - 1][player_x] == 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and maze[player_y + 1][player_x] == 0:
        player_y += 1
    if keys[pygame.K_LEFT] and maze[player_y][player_x - 1] == 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and maze[player_y][player_x + 1] == 0:
        player_x += 1

    
    clock.tick(SPEED)

pygame.quit()
