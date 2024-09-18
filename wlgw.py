import pygame
import random
import time
import threading
import sys

# 初始化 Pygame
pygame.init()
clicked_images = []  # 存储被点击的图片
# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
BG_COLOR = (255, 255, 255)
TIME_LIMIT = 30

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("蛙了个蛙")

# 加载图片
p1_image = pygame.image.load("p1.jpg")
p2_image = pygame.image.load("p2.jpg")
p3_image = pygame.image.load("p3.jpg")
p4_image = pygame.image.load("p4.jpg")
p5_image = pygame.image.load("p5.jpg")
p1_image = pygame.transform.scale(p1_image, (TILE_SIZE, TILE_SIZE))
p2_image = pygame.transform.scale(p2_image, (TILE_SIZE, TILE_SIZE))
p3_image = pygame.transform.scale(p3_image, (TILE_SIZE, TILE_SIZE))
p4_image = pygame.transform.scale(p4_image, (TILE_SIZE, TILE_SIZE))
p5_image = pygame.transform.scale(p5_image, (TILE_SIZE, TILE_SIZE))

# 初始化图片槽
image_slots = [[[random.choice([p1_image, p2_image,p3_image,p4_image,p5_image]) for _ in range(6)] for _ in range(COLS)] for _ in range(ROWS)]


# 主界面
def draw_main_screen():
    # 加载背景图片
    back_image = pygame.image.load("main.png")
    back_image = pygame.transform.scale(back_image, (WIDTH, HEIGHT))  # 确保背景图片与屏幕尺寸一致

    # 使用背景图片填充屏幕
    screen.blit(back_image, (0, 0))

    # 创建字体对象
    font = pygame.font.Font(None, 74)
    # 渲染文本
    text = font.render("VALEGEVA", True, (255, 255, 255))  # 白色文字

    # 计算文本位置
    text_rect = text.get_rect(center=(WIDTH // 2, 150))  # 将文本居中显示在屏幕上方

    # 绘制文本
    screen.blit(text, text_rect.topleft)
    # 加载开始按钮图片
    begin_image = pygame.image.load("begin.png")
    begin_image = pygame.transform.scale(begin_image, (200, 50))  # 根据需要调整按钮图片的尺寸

    # 计算按钮位置
    button_rect = pygame.Rect(WIDTH // 2 - begin_image.get_width() // 2, HEIGHT // 2 - begin_image.get_height() // 2,
                              begin_image.get_width(), begin_image.get_height())

    # 绘制按钮图片
    screen.blit(begin_image, button_rect.topleft)

    # 绘制文本
    font = pygame.font.Font(None, 74)
    text = font.render("", True, (255, 255, 255))  # 白色文字
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    main()  # 进入游戏


# 游戏界面设置
def draw_game_interface():
    screen.fill(BG_COLOR)
    # 绘制图片槽
    for row in range(ROWS):
        for col in range(COLS):
            for i in range(6):
                if row < ROWS - 1:  # 如果不是最后一行
                    image = image_slots[row][col][i]
                    screen.blit(image, (col * TILE_SIZE, row * TILE_SIZE + i * TILE_SIZE))
                else:
                    # 绘制最后一行的空白行
                    if image_slots[ROWS - 1][col] is not None:
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # 绘制第6行的点击图片
    for col in range(COLS):
        if col < len(clicked_images):
            image = clicked_images[col]
            screen.blit(image, (col * TILE_SIZE, 5 * TILE_SIZE))

    # 显示倒计时
    font = pygame.font.Font(None, 74)
    text = font.render(f"{TIME_LIMIT} Secends Remaining", True, (255, 0, 0))  # 更新倒计时显示
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    pygame.display.flip()


def handle_mouse_click(event):
    # 获取鼠标点击位置
    x, y = pygame.mouse.get_pos()
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    if col < COLS and row < ROWS:
        # 获取点击时槽中的图片
        image = image_slots[row][col][0]
        # 检查是否与 clicked_images 中最后两个图片都相同
        if len(clicked_images) >= 2 and clicked_images[-1] == image and clicked_images[-2] == image:
            print("Clicked image is the same as the last two images in clicked_images, not storing.")
            # 如果相同，从 clicked_images 中删除这两张图片
            clicked_images.pop()
            clicked_images.pop()
        else:
            # 存储点击时槽中的图片
            clicked_images.append(image)
            print("Clicked images:", clicked_images)  # 打印列表内容和长度，用于调试

def draw_end_screen():
    screen.fill(BG_COLOR)
    # 加载结束界面背景图片
    end_background = pygame.image.load("img.png")
    end_background = pygame.transform.scale(end_background, (WIDTH, HEIGHT))  # 确保背景图片与屏幕尺寸一致

    # 使用背景图片填充屏幕
    screen.blit(end_background, (0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("GAMEOVER", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))



    pygame.display.flip()

    # 等待玩家点击按钮或关闭窗口
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



# 主程序
running = True
countdown_thread = None


def countdown(t):
    global running, TIME_LIMIT
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # 设置定时器，每秒触发一次
    while t > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:  # 处理倒计时事件
                t -= 1
                TIME_LIMIT = t
                if t <= 0:
                    running = False  # 倒计时结束


def main():
    global running, TIME_LIMIT, countdown_thread
    running = True

    # 重置倒计时时间
    TIME_LIMIT = 30

    # 如果之前有正在运行的倒计时线程，则先停止它
    if countdown_thread and countdown_thread.is_alive():
        running = False  # 停止倒计时线程
        countdown_thread.join()  # 等待线程结束

    # 创建新的倒计时线程
    countdown_thread = threading.Thread(target=countdown, args=(TIME_LIMIT,))
    countdown_thread.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标点击位置
                handle_mouse_click(event)  # 调用处理函数
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                if col < COLS and row < ROWS:
                    # 切换图片槽中的图片
                    image_slots[row][col].append(image_slots[row][col].pop(0))
                    if all(all(slot[-1] == slot[0] for slot in row) for row in image_slots):
                        running = False  # 所有图片槽都显示最后一张图片时结束游戏

            elif event.type == pygame.USEREVENT + 1:  # 处理倒计时事件
                TIME_LIMIT -= 1
                if TIME_LIMIT <= 0:
                    running = False  # 倒计时结束

        if len(clicked_images) == 6:
            running = False
            draw_end_screen()
            pygame.display.flip()
            pygame.time.wait(3000)  # 等待3秒，让结束界面显示一会儿

        draw_game_interface()
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    # 倒计时结束后，绘制结束界面
    draw_end_screen()
    pygame.display.flip()
    pygame.time.wait(3000)  # 等待3秒，让结束界面显示一会儿

    # 重新开始游戏逻辑
    running = True
    # 重新创建倒计时线程
    countdown_thread = threading.Thread(target=countdown, args=(TIME_LIMIT,))
    countdown_thread.start()

    pygame.quit()  # 退出 Pygame


if __name__ == "__main__":
    draw_main_screen()

