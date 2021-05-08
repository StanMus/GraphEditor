# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.filedialog, tkinter.messagebox
from PIL import ImageTk, Image

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="red")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Графичекий редактор")
        self.parent.iconbitmap('/Users/musolov.sn/Documents/GitHub/icon.ico')
        self.parent.resizable(width=True, height=True)
        self.parent.geometry("1024x768")
        self.parent.configure() # Что значит?

        #frame1 = Frame(self.parent, width=1024, height=768, bg='#E7E6E6')
        #frame1.grid(row=0, column=0)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # консоль Файл
        fileMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=fileMenu)
        fileMenu.add_command(label="Открыть", command=self.onExit)
        fileMenu.add_command(label="Сохранить", command=self.onExit)
        fileMenu.add_command(label="Сохранить как", command=self.onExit)
        fileMenu.add_command(label="Печать", command=self.onExit)
        fileMenu.add_command(label="Экспорт", command=self.onExit)
        fileMenu.add_command(label="Свойства", command=self.onExit)
        fileMenu.add_command(label="Выход", command=self.onExit)

        # консоль Правка
        pravkaMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=pravkaMenu)
        pravkaMenu.add_command(label="Отменить действие")
        pravkaMenu.add_command(label="Повторить действие")

        # консоль Формат
        formatMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Формат", menu=formatMenu)
        formatMenu.add_command(label="Увеличить")
        formatMenu.add_command(label="Уменьшить")
        formatMenu.add_command(label="Вращение")
        formatMenu.add_command(label="Отражение")
        formatMenu.add_command(label="Коррекция яркости")
        formatMenu.add_command(label="Коррекция контрастности")
        formatMenu.add_command(label="Коррекция цветового баланса")

        filtersMenu = Menu(formatMenu, tearoff=0)
        formatMenu.add_cascade(label="Фильтры", menu=filtersMenu)
        filtersMenu.add_command(label="Черно-белый")
        filtersMenu.add_command(label="Размытие")
        filtersMenu.add_command(label="Обесцвечивание")
        filtersMenu.add_command(label="Сепия")
        filtersMenu.add_command(label="Псевдоцвет")
        filtersMenu.add_command(label="Негатив")
        filtersMenu.add_command(label="Оттенки красного")
        filtersMenu.add_command(label="Оттенки зеленого")
        filtersMenu.add_command(label="Оттенки синего")
        filtersMenu.add_command(label="Расскраска случайными цветами")
        filtersMenu.add_command(label="Винтаж")
        filtersMenu.add_command(label="Фильтр высоких частот")
        filtersMenu.add_command(label="Насыщенность")

        # консоль Справка
        helpMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=helpMenu)
        helpMenu.add_command(label="Помощь")
        helpMenu.add_command(label="О программе")

        b1 = tkinter.Button(self.parent, text='Display image', command=self.open_file)
        b1.pack(fill='x')


    def onExit(self):
        self.quit()

    def open_file(self):
        self.parent.filename = tkinter.filedialog.askopenfilename(
            parent=self.parent, initialdir='/Users/musolov.sn/Documents/GitHub/GraphEditor',
            title='Выбрать файл',
            filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png"), ('All files', '*.*'))
        )
        image_label = Label(self.parent, text=self.parent.filename)
        image_label.pack()
        my_image = ImageTk.PhotoImage(Image.open(self.parent.filename))
        my_image_label = Label(self.parent, image=my_image)
        my_image_label.pack()

def main():
    root = Tk()
    app = Example(root)
    app.mainloop()

if __name__ == '__main__':
    main()