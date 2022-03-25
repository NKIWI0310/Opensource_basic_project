import turtle
import random

## 전역 변수 선언 부분 ##
myTurtle, tX, tY, tColor, tSize, tShape = [None] * 6
shapeList = []
playerTurtles = []  # 거북 2차원 리스트
swidth, sheight = 500, 500

if __name__ == "__main__":
    turtle.title('거북 리스트 활용')
    turtle.setup(width=swidth + 50, height=sheight + 50)
    turtle.screensize(swidth, sheight)

    shape = turtle.Turtle('turtle')

    for i in range(0, 5):
        myTurtle = turtle.Turtle('turtle')

        tX = random.randrange(-80, 80)
        tY = random.randrange(-80, 80)

        r = random.random()
        g = random.random()
        b = random.random()

        tSize = random.randrange(1, 100)/10

        playerTurtles.append([myTurtle, tX, tY, tSize, r, g, b])

    for tList in playerTurtles:
        myTurtle = tList[0]
        myTurtle.color((tList[4], tList[5], tList[6]))
        myTurtle.pencolor((tList[4], tList[5], tList[6]))
        myTurtle.turtlesize(tList[3])
        myTurtle.goto(tList[1], tList[2])
    turtle.done()
