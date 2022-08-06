import Tkinter_122 as tk

root = tk.Tk()
root.geometry = "600*700"
root.title = "test"
a = root.object

def abc():
    tk.Label(root, text="Hello World", font=("Time", 10, "bold"), bg="blue").pack(pady=10)

def asd():
    print("Hello World")

def ok():
    print(entry1.get())

tk.Label(root,text = "Hello World",font = ("Time",10,"bold"), bg = "blue" ).pack(pady = 1)
tk.Label(root,text = "Hello World1",font = ("Time",10,"bold"), bg = "blue" ).pack(pady=10)
tk.Button(root, text = "click me", bg = "yellow",height =50, width=100, command= asd).pack(anchor="w",padx = 5)
entry1 = tk.Entry(root,width = 100, height = 20)
entry1.pack(pady = 5)
tk.Entry(root,width = 100, height = 20).pack(pady = 5)
tk.Button(root, text= "get your input", bg = "red", height = 50, width = 20, command=ok).pack()
frame0 = tk.Frame(root, bg = "green", width= 300, height = 50)
frame0.pack(pady = 200)
frame1= tk.Frame(root, bg = "blue", width= 300, height = 50)
frame1.pack(fill= "x")

tk.Button(frame0, bg= "pink", width = 50, height =50, text = "cick me", command= asd).pack(pady = 5)

jiba =tk.Label(frame1, text = "hello frame")
jiba.pack()
jiba1 =tk.Label(frame1, text = "hello frame")
jiba1.pack(anchor="w")
jiba2 =tk.Label(frame1, text = "hello frame")
jiba2.pack(anchor="e")

if __name__ == "__main__":

    root.mainloop()


