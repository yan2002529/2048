import pygame
from turtle import *
from random import randint
import os

# 初始化pygame的音频模块
pygame.mixer.init()

# 设置游戏窗口标题
title("2048小游戏")

# 方块大小
gz = 140
# 游戏表格的行数和列数
N = 4
# 计算游戏区域的边界长度
bc = gz * N
# 关闭动画，提高绘制效率
tracer(False)
# 设置背景颜色为浅棕色
bgcolor("#D2B48C")
# 隐藏图标
ht()
# 抬起画笔，避免绘制线条
up()
# 设置移动速度为最快
speed(0)
# 设置的形状为圆形
shape("circle")
# 调整形状大小
shapesize(4)

# 二维列表对应游戏表格
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# 记录游戏中的最大值
maxx = 2
# 记录步数
steps = 0
# 记录分数
score = 0
# 记录游戏是否暂停
paused = False

# 创建用于绘制暂停和继续按钮的Turtle对象
button_turtle = Turtle()
button_turtle.speed(0)
button_turtle.up()
button_turtle.ht()
button_turtle.color("black")  # 设置画笔颜色为黑色，用于写文字

# 创建一个用于显示步数、最大值和分数的对象
tj = Turtle()
tj.speed(0)
tj.up()
tj.ht()
tj.color("white")

# 绘制边框
def draw_border():
    penup()
    goto(-bc / 2 - 20, bc / 2 + 20)
    pendown()
    pencolor("white")
    for _ in range(2):
        forward(bc + 40)
        right(90)
        forward(20)
        right(90)
        forward(bc + 40)
        left(90)
        forward(20)
        left(90)
    penup()
    # 调整步数、最大值和分数的显示位置在边框内上方
    tj.goto(-bc / 2 + 20, bc / 2)
    tj.write("步数：{}，最大值：{}，分数：{}".format(steps, maxx, score), font=("", 20, ""))

# 绘制标题
def draw_title():
    penup()
    goto(0, bc / 2 + 60)
    pendown()
    pencolor("black")
    write("2048", font=("", 40, "bold"), align="center")
    penup()

# 颜色字典，修改为新的颜色搭配
COLORS = {
    0: "white",
    2: "#F4E76E",
    4: "#F4B084",
    8: "#F79381",
    16: "#F55D5D",
    32: "#83CAFF",
    64: "#82E0AA",
    128: "#48C9B0",
    256: "#D2B4DE",
    512: "#A3E4D7",
    1024: "#D6DBDF",
    2048: "#F7DC6F"
}

# 绘制二维列表
def draw_grid():
    global steps
    global maxx
    global score
    global paused
    if not paused:
        tj.clear()
        tj.write("步数：{}，最大值：{}，分数：{}".format(steps, maxx, score), font=("", 20, ""))
        steps += 1
        clear()
        for row in range(N):
            for col in range(N):
                # 调整方块的位置，减小间隔
                goto(-bc / 2 + gz / 2 + col * (gz + 20), bc / 2 - gz / 2 - row * (gz + 20))
                color(COLORS[grid[row][col]])
                stamp()
                sety(bc / 2 - gz / 2 - row * (gz + 20) - 30)
                color("black")
                if grid[row][col] > 0:
                    write(grid[row][col], font=("", 50, ""), align="center")
                if grid[row][col] > maxx:
                    maxx = grid[row][col]
                # 检查是否有合并情况发生，如果有则更新分数（示例简单判断相邻相同数字合并）
                if row < N - 1 and grid[row][col] == grid[row + 1][col] and grid[row][col] > 0:
                    score += grid[row][col] * 2
                if col < N - 1 and grid[row][col] == grid[row][col + 1] and grid[row][col] > 0:
                    score += grid[row][col] * 2
        update()
        if maxx == 2048:
            goto(0, 0)
            color("red")
            write("游戏胜利", font=("", 100, ""), align="center")

# 检查是否可以添加新数字
def can_add():
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                return True
    return False

# 生成随机数字
def generate_random():
    if can_add():
        added = False
        while not added:
            i = randint(0, N - 1)
            j = randint(0, N - 1)
            if grid[i][j] == 0:
                grid[i][j] = 2
                added = True

# 初始化游戏，生成第一个随机数字
generate_random()
draw_title()  # 绘制标题
draw_border()
draw_grid()

# 获取当前代码文件所在的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接音乐文件路径
music_path = os.path.join(current_dir, "2048music.mp3")

# 加载音乐文件
pygame.mixer.music.load(music_path)
# 设置音乐音量（可根据需要调整，取值范围0.0 - 1.0）
pygame.mixer.music.set_volume(0.5)
# 循环播放背景音乐
pygame.mixer.music.play(-1)

# 绘制暂停按钮（浅黄色椭圆形）
def draw_pause_button():
    button_turtle.penup()
    button_turtle.goto(-bc / 2 + 20 - 40, bc / 2 - 20)
    button_turtle.pendown()
    button_turtle.begin_fill()
    button_turtle.fillcolor("#FFFFE0")  # 设置填充颜色为浅黄色
    button_turtle.circle(20, 180)
    button_turtle.forward(40)
    button_turtle.circle(20, 180)
    button_turtle.end_fill()
    button_turtle.penup()
    button_turtle.goto(-bc / 2 + 20 - 40, bc / 2 - 40)  # 将文字位置调整到按钮正下方
    button_turtle.write("暂停", font=("", 12, ""), align="center")
    button_turtle.color("black")

# 绘制继续按钮（浅黄色椭圆形，初始隐藏）
def draw_continue_button():
    button_turtle.penup()
    button_turtle.goto(-bc / 2 + 20 - 40, bc / 2 - 80)
    button_turtle.pendown()
    button_turtle.begin_fill()
    button_turtle.fillcolor("#FFFFE0")  # 设置填充颜色为浅黄色
    button_turtle.circle(20, 180)
    button_turtle.forward(40)
    button_turtle.circle(20, 180)
    button_turtle.end_fill()
    button_turtle.penup()
    button_turtle.goto(-bc / 2 + 20 - 40, bc / 2 - 100)  # 将文字位置调整到按钮正下方
    button_turtle.write("继续", font=("", 12, ""), align="center")
    button_turtle.color("black")
    button_turtle.hideturtle()

# 定义暂停游戏的函数
def pause_game():
    global paused
    paused = True
    pygame.mixer.music.pause()  # 暂停背景音乐
    # 隐藏暂停按钮，显示继续按钮
    button_turtle.clear()
    draw_continue_button()

# 定义继续游戏的函数
def continue_game():
    global paused
    paused = False
    pygame.mixer.music.unpause()  # 恢复背景音乐
    # 隐藏继续按钮，显示暂停按钮
    button_turtle.clear()
    draw_pause_button()



# 定义点击事件处理函数
def on_click(x, y):
    global paused
    if -bc / 2 + 20 - 40 - 20 < x < -bc / 2 + 20 - 40 + 20 and bc / 2 - 20 - 20 < y < bc / 2 - 20 + 20:
        pause_game()
    elif -bc / 2 + 20 - 40 - 20 < x < -bc / 2 + 20 - 40 + 20 and bc / 2 - 80 - 20 < y < bc / 2 - 80 + 20:
        continue_game()

# 绑定点击事件
onscreenclick(on_click)

# 绘制暂停按钮
draw_pause_button()

# 定义上移函数
def up():
    global score
    global paused
    if not paused:
        # 上移逻辑
        for col in range(N):
            for row in range(1, N):
                value = grid[row][col]
                r = row
                while r > 0 and grid[r - 1][col] == 0:
                    r = r - 1
                if r - 1 >= 0 and grid[r - 1][col] == value:
                    r = r - 1
                    score += value * 2
                if r != row:
                    grid[r][col] += value
                    grid[row][col] = 0
        generate_random()
        draw_grid()

# 定义下移函数
def down():
    global score
    global paused
    if not paused:
        # 下移逻辑
        for col in range(N):
            for row in range(N - 2, -1, -1):
                value = grid[row][col]
                r = row
                while r < N - 1 and grid[r + 1][col] == 0:
                    r = r + 1
                if r + 1 < N and grid[r + 1][col] == value:
                    r = r + 1
                    score += value * 2
                if r != row:
                    grid[r][col] += value
                    grid[row][col] = 0
        generate_random()
        draw_grid()

# 定义左移函数
def left():
    global score
    global paused
    if not paused:
        # 左移逻辑
        for row in range(N):
            for col in range(1, N):
                value = grid[row][col]
                c = col
                while c > 0 and grid[row][c - 1] == 0:
                    c = c - 1
                if c - 1 >= 0 and grid[row][c - 1] == value:
                    c = c - 1
                    score += value * 2
                if c != col:
                    grid[row][c] += value
                    grid[row][col] = 0
        generate_random()
        draw_grid()

# 定义右移函数
def right():
    global score
    global paused
    if not paused:
        # 右移逻辑
        for row in range(N):
            for col in range(N - 2, -1, -1):
                value = grid[row][col]
                c = col
                while c < N - 1 and grid[row][c + 1] == 0:
                    c = c + 1
                if c + 1 < N and grid[row][c + 1] == value:
                    c = c + 1
                    score += value * 2
                if c != col:
                    grid[row][c] += value
                    grid[row][col] = 0
        generate_random()
        draw_grid()

# 绑定键盘事件
onkeypress(up, "Up")
onkeypress(down, "Down")
onkeypress(left, "Left")
onkeypress(right, "Right")
listen()

# 结束绘制
done()
