# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.filedialog, tkinter.messagebox

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="blue")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Шифратор и дешифратор на основе алгоритма «Блокнот»")
        self.parent.iconbitmap(u'main.ico')
        self.parent.resizable(width=False, height=False)
        self.parent.configure() # Что значит?

        frame1 = Frame(self.parent, width=780, height=410, bg='#E7E6E6')
        frame1.grid(row=0, column=0)
        label1 = Label(frame1, text='Исходный текст:', bg='#E7E6E6', font="Verdana 11")
        label1.place(x=30, y=10, width=340)
        self.txt2cod = Text(frame1, bg='white', font="Verdana 11", wrap=WORD)
        self.txt2cod.config(state=NORMAL)
        self.txt2cod.place(x=30, y=35, width=340, height=220)
        label2 = Label(frame1, text='Криптограмма:', bg='#E7E6E6', font="Verdana 11")
        label2.place(x=410, y=10, width=340)
        self.output = Text(frame1, bg="white", font="Verdana 11", wrap=WORD)
        self.output.config(state=NORMAL)
        self.output.place(x=410, y=35, width=340, height=220)

        label3 = Label(frame1, text='Словарь:', bg='#E7E6E6', font="Verdana 11")
        label3.place(x=30, y=365, width=70, height=25)
        self.libEntry = Entry(frame1, bg="white", bd=0, font="Verdana 11")
        self.libEntry.insert(END, 'dictionary.txt')
        self.libEntry.place(x=120, y=365, width=120, height=25)

def main():
    root = Tk()
    app = Example(root)
    app.mainloop()

if __name__ == '__main__':
    main()
