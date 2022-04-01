import turtle
import random
import math
from tkinter.simpledialog import *

#2019038024 이동민

swidth, sheight = 500, 500
txtSize = 20
turn = 2

turtle.title('거북이가 나선 모양의 글자쓰기')
turtle.shape('turtle')
turtle.setup(width=swidth + 50, height=sheight + 50)
turtle.screensize(swidth, sheight)
turtle.penup()

inStr = askstring('문자열 입력', '거북이가 쓸 문자열을 입력')
count = len(inStr)
angle = 360 * turn / count
CL = 250
SC = 250
Li = 250 / count

for ch in inStr:
    CL -= Li
    SC -= angle
    x = CL * math.cos(math.radians(SC))
    y = CL * math.sin(math.radians(SC))
    turtle.goto(x, y)
    r = random.random();
    g = random.random();
    b = random.random()
    turtle.pencolor((r, g, b))
    turtle.write(ch)

turtle.done()
