from tkinter import *

from tkinter import messagebox

top = Tk()
top.geometry("500x500")


# Function to show abort message box
def abortMessageCallBack():
    msg = messagebox.askyesno("Abort Mission?", "Do you really want to abort the mission?")


# Function to show verify message box
def verifyMessageCallBack():
    msg = messagebox.askyesno("Verify Launch", "Do you want to verify for launch?")


# Abort Mission Button
abortButton = Button(top, text="ABORT MISSION", bg="red", command=abortMessageCallBack)
abortButton.place(x=50, y=350)

# Verify Launch Button
verifyButton = Button(top, text="Verify Launch", bg="green", command=verifyMessageCallBack)
verifyButton.place(x=50, y=400)

top.mainloop()
