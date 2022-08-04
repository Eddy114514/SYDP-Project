import Tkinter_122 as tk

root = tk.Tk()
root.geometry = "600*700"
root.title = "test"
a = root.object

def abc():
    tk.Label(root, text="Hello World", font=("Time", 10, "bold"), bg="blue").pack(pady=10)

def asd():
    print("secondbutton")


tk.Label(root,text = "Hello World",font = ("Time",10,"bold"), bg = "blue" ).pack(pady = 10 )


if __name__ == "__main__":

    root.mainloop()


