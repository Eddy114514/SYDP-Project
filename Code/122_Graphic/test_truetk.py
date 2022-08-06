import tkinter as tk
root = tk.Tk()
root.geometry("500x500")
root.title = "test"

def abc():
    tk.Label(root, text="Hello World", font=("Time", 10, "bold"), bg="blue").pack(pady=10)

def asd():
    print("Hello World")

def ok():
    print(entry1.get())

tk.Label(root,text = "Hello World",font = ("Time",10,"bold"), bg = "blue" ).pack(pady = 1)
tk.Label(root,text = "Hello World1",font = ("Time",10,"bold"), bg = "blue" ).pack(pady=10)
tk.Button(root, text = "click me", bg = "yellow",height =5, width=10, command= asd).pack(anchor="w",padx = 5)
entry1 = tk.Entry(root)
entry1.pack(pady = 5)
tk.Entry(root).pack(pady = 5)
tk.Button(root, text= "get your input", bg = "red", height = 5, width = 20, command=ok).pack()


if __name__ == "__main__":

    root.mainloop()


