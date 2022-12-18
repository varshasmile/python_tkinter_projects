from tkinter import *
root = Tk()

def myClick():
    myLabel = Label(root, text="You Clicked the Button!")
    myLabel.pack()

myButton = Button(root, text="Click Me!", command=myClick, fg="orange", bg="yellow")
myButton2 = Button(root, text="Click Me!", padx=50, pady=30, command=myClick, fg="white", bg="red")  #Increases the size of the button
myButton3 = Button(root, text="Don't Click Me!", state=DISABLED, fg="green") #Disables the button
myButton.pack()
myButton2.pack()
myButton3.pack()

root.mainloop()