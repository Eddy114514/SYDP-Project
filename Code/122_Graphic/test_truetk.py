from tkinter import *

root = Tk()
root.title("Test1")
root.geometry("500x500")
Label(bg="red",text = "hellow world", font= ("Time",10,"bold")).pack(pady=1)
Label(bg="red",text = "hellow world", font= ("Time",10,"bold")).pack(anchor="w")
Label(bg="red",text = "hellow world", font= ("Time",10,"bold")).pack(anchor="e")
Label(bg="red",text = "hellow world", font= ("Time",10,"bold")).pack()



if __name__ == "__main__":

    root.mainloop()