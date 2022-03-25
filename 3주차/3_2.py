import turtle
import math
import random

t1, t2, t2 = [None] *3
t1X,t1Y,t2X,t2Y,t3X,t3Y = [0] *6

if __name__ == "__main__":
    turtle.title('거북이 만나기')

    t1 = turtle.Turtle('turtle'); t1.color('red'); t1.penup()
    t2 = turtle.Turtle('turtle'); t2.color('green'); t2.penup()
    t3 = turtle.Turtle('turtle'); t3.color('blue'); t3.penup()

    t1.goto(100,100); t2.goto(0,0); t3.goto(-100,-100)
#2019038024 이동민
    while True:
        angle = random.randrange(0,360)
        dist = random.randrange(1,50)
        t1.left(angle); t1.forward(dist)

        angle = random.randrange(0,360)
        dist = random.randrange(1,50)
        t2.left(angle); t2.forward(dist)

        angle = random.randrange(0, 360)
        dist = random.randrange(1, 50)
        t3.left(angle); t3.forward(dist)

        t1X = t1.xcor(); t1Y = t1.ycor()
        t2X = t2.xcor(); t2Y = t2.ycor()
        t3X = t3.xcor(); t3Y = t3.ycor()

        if abs(t1X - t2X) < 10 and abs(t1Y - t2Y) <10 or \
            abs(t2X - t3X) < 10 and abs(t2Y - t3Y) <10 or \
            abs(t1X - t3X) < 10 and abs(t1Y - t3Y) < 10:
            t1.turtlesize(3); t2.turtlesize(3); t3.turtlesize(3)
            break
turtle.done()