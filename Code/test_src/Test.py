from tkinter import *

root = Tk()
root.geometry("200x200")



a = Button(root, text="click", command= lambda :[a.configure(bg="red") if a.cget("bg") != "red" else a.configure(bg="SystemButtonFace")])
a.pack()

root.mainloop()

