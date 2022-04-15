from tkinter import *

#2019038024 이동민

def KeyClick(e):
    global key
    key=e.keysym
    if key=='Up':    #KEY값이 위쪽아면
        func_zoom()
    elif key=='Down':   #KEY값이 아래쪽이면
        func_sub()

def func_zoom():
    global photo
    photo = photo.zoom(2,2)
    label.configure(image = photo)
    label.image = photo

def func_sub():
    global photo
    photo = photo.subsample(2,2)
    label.configure(image = photo)
    label.image = photo

window = Tk()
window.title("연습문제")
window.geometry("400x400")
photo = PhotoImage(file="C:/Users/이동민/OneDrive/바탕 화면/dog.gif")
label = Label(window, image = photo)
label.pack(anchor=CENTER)

window.bind("<Key>",KeyClick)

mainMenu = Menu(window)
window.config(menu=mainMenu)
fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)

window.mainloop()