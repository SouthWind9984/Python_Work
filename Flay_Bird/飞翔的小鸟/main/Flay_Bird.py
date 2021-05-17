# coding=utf-8
import pygame
from pygame.locals import *
import sys
import random

# 常量设置
Screen_WIDTH = 288
Screen_HEIGHT = 512
FPS = 30

# 初始化
pygame.init()
pygame.font.init()
pygame.mixer.init()
# 创建窗体
screen = pygame.display.set_mode((Screen_WIDTH, Screen_HEIGHT))
# 设置标题
pygame.display.set_caption("Flappy Bird By_小小怪")

# 加载图片
backGround_day_img = pygame.image.load("../rec/sprites/background-day.png").convert_alpha()
backGround_night_img = pygame.image.load("../rec/sprites/background-night.png").convert_alpha()
start_message = pygame.image.load("../rec/sprites/message.png").convert_alpha()
base_img = pygame.image.load("../rec/sprites/base.png").convert_alpha()
screen.blit(backGround_day_img, (0, 0))
screen.blit(start_message, (55, 80))
screen.blit(base_img, (Screen_WIDTH - base_img.get_width(), Screen_HEIGHT - base_img.get_height()))

Game_over = pygame.image.load("../rec/sprites/gameover.png").convert_alpha()
nums_img = (
    pygame.image.load('../rec/sprites/0.png').convert_alpha(),
    pygame.image.load('../rec/sprites/1.png').convert_alpha(),
    pygame.image.load('../rec/sprites/2.png').convert_alpha(),
    pygame.image.load('../rec/sprites/3.png').convert_alpha(),
    pygame.image.load('../rec/sprites/4.png').convert_alpha(),
    pygame.image.load('../rec/sprites/5.png').convert_alpha(),
    pygame.image.load('../rec/sprites/6.png').convert_alpha(),
    pygame.image.load('../rec/sprites/7.png').convert_alpha(),
    pygame.image.load('../rec/sprites/8.png').convert_alpha(),
    pygame.image.load('../rec/sprites/9.png').convert_alpha()
)
# 小鸟图片
bird_mid1 = pygame.image.load("../rec/sprites/bluebird-midflap.png").convert_alpha()
bird_up1 = pygame.image.load("../rec/sprites/bluebird-upflap.png").convert_alpha()
bird_down1 = pygame.image.load("../rec/sprites/bluebird-downflap.png").convert_alpha()
bird_mid2 = pygame.image.load("../rec/sprites/redbird-midflap.png").convert_alpha()
bird_up2 = pygame.image.load("../rec/sprites/redbird-upflap.png").convert_alpha()
bird_down2 = pygame.image.load("../rec/sprites/redbird-downflap.png").convert_alpha()
bird_mid3 = pygame.image.load("../rec/sprites/yellowbird-midflap.png").convert_alpha()
bird_up3 = pygame.image.load("../rec/sprites/yellowbird-upflap.png").convert_alpha()
bird_down3 = pygame.image.load("../rec/sprites/yellowbird-downflap.png").convert_alpha()
bird1 = [bird_up1, bird_mid1, bird_down1]
bird2 = [bird_up2, bird_mid2, bird_down2]
bird3 = [bird_up3, bird_mid3, bird_down3]
bird = [bird1, bird2, bird3]
# 柱子图片
pipe_green = pygame.image.load("../rec/sprites/pipe-green.png").convert_alpha()
pipe_green_2 = pygame.transform.flip(pipe_green, False, True)
pipe_red = pygame.image.load("../rec/sprites/pipe-red.png").convert_alpha()
pipe_red2 = pygame.transform.flip(pipe_red, False, True)
pipe_img = [[pipe_green, pipe_green_2], [pipe_red, pipe_red2]]

# 加载音频
wing_audio = pygame.mixer.Sound("../rec/audio/wing.wav")
point_audio = pygame.mixer.Sound("../rec/audio/point.wav")
die_audio = pygame.mixer.Sound("../rec/audio/die.wav")
hit_audio = pygame.mixer.Sound("../rec/audio/hit.wav")
# 游戏帧数
clock = pygame.time.Clock()


def showBackGround(x):
    if x == 0:
        screen.blit(backGround_day_img, (0, 0))
    else:
        screen.blit(backGround_night_img, (0, 0))


# 显示开始的草地
def showBaseImg(w):
    screen.blit(base_img, (w, Screen_HEIGHT - base_img.get_height()))
    if w >= Screen_WIDTH - base_img.get_width() + 3:
        w -= 3
    else:
        w = 0
    return w





# 模拟小鸟运动
def showFlyBirdUP(x, y):
    screen.blit(bird[n][0], (x, y))
    y -= 35
    return y


def showFlyBirdDown(x, y):
    screen.blit(bird[n][2], (x, y))
    y += 3
    return y

def showFlyBidMid(x, y):
    screen.blit(bird[n][1], (x, y))


# 小鸟震动范围 8
def showFlyBrid(f, x, y):
    # 0上 1停 2下
    if f == 0:
        y -= 1
        screen.blit(bird[n][0], (x, y))
        return y
    elif f == 1:
        y += 5
        screen.blit(bird[n][1], (x, y))
        return y
    elif f == 2:
        y += 15
        screen.blit(bird[n][2], (x, y))
        return y


# 显示柱子
def showPipe(index, x, y):
    screen.blit(pipe_img[index][1], (x, y - pipe_green.get_height()))
    screen.blit(pipe_img[index][0], (x, y + 100))
    x -= 2
    return x


# 触碰事件：
"""
碰到柱子，天花板，地面 游戏结束
"""


def die(y, x1, y1):
    if y >= Screen_HEIGHT - base_img.get_height() - bird[n][0].get_height():
        return True
    if y <= 0:
        return True
    if 60 - pipe_green.get_width() < x1 < 60 + bird[n][0].get_width():
        if y <= y1 or y >= y1 + 100 - bird[n][0].get_height():
            return True


def main():
    # 变量
    global source
    base_width = 0
    brid_y = 250
    brid_x = 60
    pipe_x = 290
    pipe_y = random.randint(50, 270)
    flag = False  # 真为开始游戏，
    over = False  # 真为游戏结束
    source = 0
    nums_y = 20
    background_x = 0
    index = random.randint(0, 1)
    # 随机挑选一只小鸟游戏
    global n
    n = random.randint(0,2)
    # 业务逻辑
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_press = pygame.mouse.get_pressed()
                if mouse_press[0] == 1:
                    flag = True
                    if over:
                        main()
                if mouse_press[2] is True:
                    print("右键")
            if event.type == KEYDOWN:
                if flag == True and (event.key == K_UP or event.key == K_SPACE):
                    brid_y = showFlyBirdUP(brid_x, brid_y)
                    # brid_y = showFlyBrid(1,brid_x,brid_y)
                    wing_audio.play()

        # 背景
        showBackGround(background_x)
        if over:
            showBackGround(1)
        if not flag and not over:
            screen.blit(start_message, (55, 80))
            # 震动翅膀
            if 220 <= brid_y < 240 or 240 < brid_y <= 250:
                brid_y = showFlyBrid(0, brid_x, brid_y)
            elif brid_y == 240:
                brid_y = showFlyBrid(1, brid_x, brid_y)
            else:
                brid_y = showFlyBrid(2, brid_x, brid_y)
        if flag and not over:
            brid_y = showFlyBirdDown(brid_x, brid_y)
            # brid_y = showFlyBrid(2,brid_x,brid_y)
            pipe_x = showPipe(index, pipe_x, pipe_y)
            if pipe_x <= -pipe_green.get_width():
                pipe_x = 290
                pipe_y = random.randint(50, 270)
                index = random.randint(0, 1)
                print(pipe_y)
            if pipe_x == 50 - pipe_green.get_width():
                source = source + 1
                point_audio.play()
            if die(brid_y, pipe_x, pipe_y):
                print("Game Over!!!")
                hit_audio.play()
                die_audio.play()
                over = True
                flag = False
        if over:
            showPipe(index, pipe_x, pipe_y)
            if brid_y < Screen_HEIGHT-base_img.get_height()-bird[n][0].get_height():
                brid_y = showFlyBirdDown(brid_x, brid_y)
            else:
                showFlyBirdDown(brid_x, brid_y)
            screen.blit(Game_over, (50, 180))
        nums_x = 125
        m = source
        if m < 10:
            screen.blit(nums_img[m], (nums_x, nums_y))
        else:
            while m > 0:
                nums_x += 5
                screen.blit(nums_img[m % 10], (nums_x, nums_y))
                nums_x -= 25
                m = m // 10
        if over:
            showBaseImg(base_width)
        else:
            base_width = showBaseImg(base_width)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
