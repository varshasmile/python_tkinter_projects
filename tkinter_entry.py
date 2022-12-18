from tkinter import *
root = Tk()

e = Entry(root, width=50, fg="white", bg="blue", borderwidth=5)
e.pack()
e.insert(0, "Enter Your Name")

def myClick():
    hello = f"Welcome, {e.get()}!"
    myLabel = Label(root, text=hello)
    myLabel.pack()

myButton = Button(root, text="Click Here!", command=myClick, fg="red", bg="yellow", borderwidth=3)
myButton.pack()


root.mainloop()