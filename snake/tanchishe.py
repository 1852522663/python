import pygame
import random

# 游戏窗口尺寸
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# 蛇身格子大小和初始位置
CELL_SIZE = 20
INITIAL_POS_X = WINDOW_WIDTH // 2
INITIAL_POS_Y = WINDOW_HEIGHT // 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 定义方向常量
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# 初始化pygame
pygame.init()

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇')

clock = pygame.time.Clock()

# 游戏结束标志
game_over = False

# 初始化蛇的位置和初始长度
snake = [(INITIAL_POS_X, INITIAL_POS_Y)]
snake_direction = RIGHT

# 生成食物的位置
food_x = random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE
food_y = random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE

# 初始化得分
score = 0

# 创建字体对象
font = pygame.font.Font(None, 30)

# 游戏主循环
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != DOWN:
                snake_direction = UP
            elif event.key == pygame.K_DOWN and snake_direction != UP:
                snake_direction = DOWN
            elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                snake_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                snake_direction = RIGHT

    # 更新蛇的位置
    head_x, head_y = snake[0]
    if snake_direction == UP:
        new_head = (head_x, head_y - CELL_SIZE)
    elif snake_direction == DOWN:
        new_head = (head_x, head_y + CELL_SIZE)
    elif snake_direction == LEFT:
        new_head = (head_x - CELL_SIZE, head_y)
    elif snake_direction == RIGHT:
        new_head = (head_x + CELL_SIZE, head_y)

    snake.insert(0, new_head)

    # 判断是否吃到食物
    if new_head[0] == food_x and new_head[1] == food_y:
        # 生成新的食物位置
        food_x = random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE
        food_y = random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE
        # 增加得分
        score += 1
    else:
        # 如果没有吃到食物，移除蛇尾
        snake.pop()

    # 判断蛇是否撞墙
    if (
        new_head[0] < 0
        or new_head[0] >= WINDOW_WIDTH
        or new_head[1] < 0
        or new_head[1] >= WINDOW_HEIGHT
    ):
        game_over = True

    # 判断蛇是否撞到自己的身体
    if new_head in snake[1:]:
        game_over = True

    # 绘制游戏窗口
    window.fill(BLACK)

    # 绘制蛇
    for (x, y) in snake:
        pygame.draw.rect(window, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

    # 绘制食物
    pygame.draw.rect(window, RED, (food_x, food_y, CELL_SIZE, CELL_SIZE))

    # 绘制得分
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    # 更新窗口显示
    pygame.display.update()

    # 控制游戏帧率
    clock.tick(10)

# 游戏结束后显示最终得分和"Game Over"
game_over_text = font.render("Game Over", True, WHITE)
score_text = font.render("Final Score: " + str(score), True, WHITE)
restart_text = font.render("Click to restart", True, WHITE)

# 居中绘制文本
game_over_text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))

# 绘制游戏窗口
window.fill(BLACK)
window.blit(game_over_text, game_over_text_rect)
window.blit(score_text, score_text_rect)
window.blit(restart_text, restart_text_rect)
pygame.display.update()

# 等待用户重新开始游戏

restart = False
while not restart:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            restart = True  # Exit the restart loop if the user quits
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_text_rect.collidepoint(mouse_x, mouse_y):
                # Reset the game state
                snake = [(INITIAL_POS_X, INITIAL_POS_Y)]
                snake_direction = RIGHT
                food_x = random.randint(0, WINDOW_WIDTH // CELL_SIZE - 1) * CELL_SIZE
                food_y = random.randint(0, WINDOW_HEIGHT // CELL_SIZE - 1) * CELL_SIZE
                score = 0
                game_over = False  # Reset the game over flag
                restart = True
