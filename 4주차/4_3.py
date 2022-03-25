import turtle
import random

myturtle, tx, ty, tcolor, tsize, tshape = [None] * 6
shapelist = []
playerturtles = []
swidth, sheight = 500, 500

#2019038024 이동민

if __name__ == "__main__":
    turtle.title('거북이 리스트 활용 (정렬)')
    turtle.setup(width=swidth + 50, height=sheight + 50)
    turtle.screensize(swidth, sheight)

    for i in range(0, 5):

        myturtle = turtle.Turtle('turtle')
        tx = random.randrange(-swidth / 2, swidth / 2)
        ty = random.randrange(-sheight / 2, sheight / 2)
        r = random.random();
        g = random.random();
        b = random.random()
        tsize = random.randrange(1, 100)/10
        playerturtles.append([myturtle, tx, ty, tsize, r, g, b])

    for i in range(0, len(playerturtles) - 1): #크기가 큰 거북이가 누굴지 저장
        for k in range(i + 1, len(playerturtles)):
            iVal = playerturtles[i][3]
            kVal = playerturtles[k][3]
            if iVal > kVal:
                playerturtles[i], playerturtles[k] = playerturtles[k], playerturtles[i]

    savex, savey = playerturtles[0][1], playerturtles[0][2] #위치 저장

    for tlist in playerturtles:
        myturtle = tlist[0]
        myturtle.penup()
        myturtle.goto(savex, savey)
        myturtle.color((tlist[4], tlist[5], tlist[6]))
        myturtle.pencolor((tlist[4], tlist[5], tlist[6]))
        myturtle.turtlesize(tlist[3])
        myturtle.pendown()
        myturtle.goto(tlist[1], tlist[2])
        savex = tlist[1]
        savey = tlist[2]

    turtle.done()
