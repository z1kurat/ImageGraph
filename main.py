import tkinter

from View.CustomTkinter import Application

root = tkinter.Tk()
root.title("Контурус")
root.geometry("1080x720")
root.attributes("-fullscreen", False)

app = Application(master=root)


app.mainloop()
