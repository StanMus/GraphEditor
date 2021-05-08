# -*- coding: utf-8 -*-
import tkinter, PIL
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Графичекий редактор")
        self.parent.iconbitmap('/Users/musolov.sn/Documents/GitHub/icon.ico')
        self.parent.resizable(width=True, height=True)
        self.parent.geometry("1024x768")
        self.parent.configure()  # Что значит?

        self.initMenubar()
        self.initFrames()

    def initMenubar(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=fileMenu)
        fileMenu.add_command(label="Загрузить", command=self.open_file)

    def initFrames(self):
        framePicture = Frame(self.parent, name='framePicture')
        framePicture.place(x=0, y=0,
                        relwidth=0.85, relheight=1)
        frameTools = Frame(self.parent, name='frameTools')

        frameTools.place(relx=0.85, rely=0,
                        relwidth=0.15, relheight=1)

        b1 = Button(frameTools, text='Display image', command=self.open_file)
        b1.pack(side=TOP)

    def open_file(self):
        filename = filedialog.askopenfilename(
            initialdir='/Users/musolov.sn/Documents/GitHub/GraphEditor',
            title='Выбрать файл',
            filetypes=(("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("gif files", "*.gif*"), ("png files", "*.png"))
        )

        framePicture = self.parent.nametowidget('framePicture')
        for widget in framePicture.winfo_children():
            widget.destroy()

        canvas=Canvas(framePicture, width=500, height=500, \
                    background="gray")
        canvas.pack()

        #image_label = Label(framePicture, text=filename)
        #image_label.pack()
        my_image0 = ImageTk.PhotoImage(Image.open(filename))
        my_image = Image.open(filename)
        my_image1 = ImageTk.PhotoImage(my_image)
        canvas.create_image(0, 0, anchor='nw', image=my_image1)


def main():
    root = Tk()
    app = Example(root)
    app.mainloop()

if __name__ == '__main__':
    main()