import turtle

swidth, sheight = 0, 0

turtle.shape('turtle')

x=0;y=0

#2019038024 이동민

if __name__ == "__main__":
    for i in range(2,10):
     for k in range(1,10):
         result=i*k
         turtle.penup()
         turtle.goto(x,y)
         turtle.pendown()
         result_a = str(i) + 'X' + str(k)  + '=' +str(i*k)
         turtle.write(result_a)
         y-=10
     x+=50;y=sheight/2

turtle.done()