from tkinter import *

OPTIONS = [
    "model_1",
    "model_2",
    "model_3"
]

root = Tk()
root.title("DropdownList - Demo OptionMenu")
root.geometry("300x150")

variable = StringVar(root)
variable.set(OPTIONS[0])

w = OptionMenu(root, variable, *OPTIONS)
w.pack(pady=20)

def ok():
    print("Value is:", variable.get())

button = Button(root, text="OK", command=ok)
button.pack()

mainloop()
