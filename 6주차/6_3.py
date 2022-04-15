from tkinter import *
from tkinter import ttk

#2019038024 이동민
window = Tk()
window.iconbitmap()
baseTab = ttk.Notebook(window)
tabDog = ttk.Frame(baseTab)
baseTab.add(tabDog, text='강아지')
tabCat = ttk.Frame(baseTab)
baseTab.add(tabCat, text='고양이')
baseTab.pack(expand=1, fill="both")
photoDog = PhotoImage(file="C:/Users/이동민/OneDrive/바탕 화면/dog.gif")
labelDog = Label(tabDog, image=photoDog)
labelDog.pack()
photoCat = PhotoImage(file="C:/Users/이동민/OneDrive/바탕 화면/cat.gif")
labelCat = Label(tabCat, image=photoCat)
labelCat.pack()
window.mainloop()
