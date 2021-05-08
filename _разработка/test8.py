# -*- coding: utf-8 -*-
import tkinter, PIL
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageOps, ImageEnhance
import os
import ctypes
import imghdr
from collections import *

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
        self.initButtons()

    def initMenubar(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # консоль Файл
        fileMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=fileMenu)
        fileMenu.add_command(label="Открыть", command=self.newImage)
        fileMenu.add_command(label="Сохранить", command=self.save)
        fileMenu.add_command(label="Сохранить как", command=self.saveAs)
        # fileMenu.add_command(label="Печать", command=onExit(root))
        # fileMenu.add_command(label="Экспорт", command=onExit(root))
        # fileMenu.add_command(label="Свойства", command=onExit(root))
        fileMenu.add_command(label="Выход", command=self.onExit)

        # консоль Правка
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Отменить действие", command=self.undo)
        editmenu.add_command(label="Выполнить действие", command=self.redo)
        editmenu.add_command(label="Отменить все", command=self.reset)
        menubar.add_cascade(label="Правка", menu=editmenu)

        # консоль Формат
        formatMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Формат", menu=formatMenu)
        #formatMenu.add_command(label="Вращение", command=rotate(canvas))
        formatMenu.add_command(label="Отражение (горизонтально)", command=self.mirror)
        formatMenu.add_command(label="Отражение (вертикально)", command=self.flip)
        formatMenu.add_command(label="Коррекция яркости", command=self.brightness)
        formatMenu.add_command(label="Коррекция контрастности")
        formatMenu.add_command(label="Коррекция цветового баланса")

        # консоль Фильтры
        filtersMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Фильтры", menu=filtersMenu)
        filtersMenu.add_command(label="Черно-белый", command=self.convertGray)
        filtersMenu.add_command(label="Инверсия", command=self.invert)
        filtersMenu.add_command(label="Размытие")
        filtersMenu.add_command(label="Обесцвечивание")
        filtersMenu.add_command(label="Сепия", command=self.sepia)
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

    def initButtons(self):
        backgroundColour = "white"
        buttonWidth = 14
        buttonHeight = 2
        toolKitFrame = Frame(self.parent, name='frameTools')
        toolKitFrame.place(relx=0.85, rely=0,
                           relwidth=0.15, relheight=1)

        toolKitFrameInside = Frame(toolKitFrame)
        toolKitFrameInside.pack()
        mirrorButton = Button(toolKitFrameInside, text="Mirror", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.mirror)
        mirrorButton.grid(row=0, column=0)

    def initFrames(self):
        canvasWidth = 850
        canvasHeight = 750
        self.parent.framePicture = Frame(self.parent, name='framePicture')
        self.parent.framePicture.place(x=0, y=0,
                           relwidth=0.85, relheight=1)
        self.parent.canvas = Canvas(self.parent.framePicture, width=canvasWidth, height=canvasHeight, \
                        background="gray")

        xsb = Scrollbar(self.parent.framePicture, orient="horizontal", command=self.parent.canvas.xview)
        ysb = Scrollbar(self.parent.framePicture, orient="vertical", command=self.parent.canvas.yview)
        self.parent.canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.parent.canvas.configure(scrollregion=(0, 0, 850, 750))

        xsb.grid(row=1, column=0, sticky="ew")
        ysb.grid(row=0, column=1, sticky="ns")
        self.parent.canvas.grid(row=0, column=0, sticky="nsew")
        self.parent.framePicture.grid_rowconfigure(0, weight=1)
        self.parent.framePicture.grid_columnconfigure(0, weight=1)

        # This is what enables using the mouse:
        self.parent.canvas.bind("<ButtonPress-1>", self.move_start)
        self.parent.canvas.bind("<B1-Motion>", self.move_move)
        # windows scroll
        self.parent.canvas.bind("<MouseWheel>", self.zoomer)

        # Set up canvas data and call init
        class Struct: pass

        self.parent.canvas.data = Struct()
        self.parent.canvas.data.width = canvasWidth
        self.parent.canvas.data.height = canvasHeight
        self.parent.canvas.data.mainWindow = self.parent.framePicture
        self.init()
        self.parent.bind("<Key>", self.keyPressed)

    def init(self):
        self.parent.canvas.data.image = None
        self.parent.canvas.data.imageAfterScale = None
        self.parent.canvas.data.currentImage = None
        self.parent.canvas.data.scaleRatio = 1
        self.parent.canvas.data.angleSelected = None
        self.parent.canvas.data.rotateWindowClose = False
        self.parent.canvas.data.brightnessWindowClose = False
        self.parent.canvas.data.brightnessLevel = 1
        self.parent.canvas.data.histWindowClose = False
        self.parent.canvas.data.solarizeWindowClose = False
        self.parent.canvas.data.posterizeWindowClose = False
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.endCrop = False
        self.parent.canvas.data.drawOn = True

        self.parent.canvas.data.undoQueue = deque([], 10)
        self.parent.canvas.data.redoQueue = deque([], 10)

    ################ METHODS ############################

    ################ FILE MENU FUNCTIONS ############################
    def newImage(self):
        imageName = filedialog.askopenfilename(
            initialdir='/Users/musolov.sn/Documents/GitHub/GraphEditor',
            title='Выбрать файл',
            filetypes=(
            ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("gif files", "*.gif*"), ("png files", "*.png"))
        )
        filetype = ""
        # make sure it's an image file
        try:
            filetype = imghdr.what(imageName)
        except:
            messagebox.showinfo(title="Выбрать файл", \
                                message="Выберите файл-изображение!", parent=self.parent.canvas.data.mainWindow)
        # restrict filetypes to .jpg, .bmp, etc.
        if filetype in ['jpeg', 'bmp', 'png', 'tiff', 'jpg']:
            self.parent.canvas.data.imageLocation = imageName
            im = Image.open(imageName)
            self.parent.canvas.data.image = im
            self.parent.canvas.data.originalImage = im.copy()
            self.parent.canvas.data.undoQueue.append(im.copy())
            self.parent.canvas.data.imageSize = im.size  # Original Image dimensions
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()
        else:
            messagebox.showinfo(title="Выбрать файл", \
                                message="Выберите файл-изображение!", parent=self.parent.canvas.data.mainWindow)

    def save(self):
        if self.parent.canvas.data.image != None:
            im = self.parent.canvas.data.image
            im.save(self.parent.canvas.data.imageLocation)

    def saveAs(self):
        # ask where the user wants to save the file
        if self.parent.canvas.data.image != None:
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=(
            ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("gif files", "*.gif*"), ("png files", "*.png"))
                                                    )
            im = self.parent.canvas.data.image
            if (filename != ''):
                im.save(filename)

    def onExit(self):
        self.quit()

    ################ EDIT MENU FUNCTIONS ############################
    def keyPressed(self, event):
        if event.keysym == "z":
            self.undo()
        elif event.keysym == "y":
            self.redo()

    # we use deques so as to make Undo and Redo more efficient and avoid
    # memory space isuues
    # after each change, we append the new version of the image to
    # the Undo queue
    def undo(self):
        if len(self.parent.canvas.data.undoQueue) > 0:
            # the last element of the Undo Deque is the
            # current version of the image
            lastImage = self.parent.canvas.data.undoQueue.pop()
            # we would want the current version if wehit redo after undo
            self.parent.canvas.data.redoQueue.appendleft(lastImage)
        if len(self.parent.canvas.data.undoQueue) > 0:
            # the previous version of the image
            self.parent.canvas.data.image = self.parent.canvas.data.undoQueue[-1]
        # save(canvas)
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def redo(self):
        if len(self.parent.canvas.data.redoQueue) > 0:
            self.parent.canvas.data.image = self.parent.canvas.data.redoQueue[0]
        # save(canvas)
        if len(self.parent.canvas.data.redoQueue) > 0:
            # we remove this version from the Redo Deque beacuase it
            # has become our current image
            lastImage = self.parent.canvas.data.redoQueue.popleft()
            self.parent.canvas.data.undoQueue.append(lastImage)
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def reset(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        ### change back to original image
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = self.parent.canvas.data.originalImage.copy()
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    ################ FORMAT MENU FUNCTIONS ############################
    # move
    def move_start(self, event):
        self.parent.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.parent.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    def zoomer(self, event):
        if (event.delta > 0):
            self.parent.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.parent.canvas.scale("all", event.x, event.y, 0.9, 0.9)

        self.scale_image(event.delta)

        self.parent.canvas.configure(scrollregion=self.parent.canvas.bbox("all"))

    def scale_image(self, delta):
        global resizedImage, im, imageForTk, imageAfterScale, imageAfterScaleNew
        scaleUp = 1.1
        scaleDown = 0.9
        scaleRatio = self.parent.canvas.data.scaleRatio
        #im = self.parent.canvas.data.image
        #imageAfterScale = self.parent.canvas.data.imageAfterScale
        #if (imageAfterScale == None):
            #scaleRatio = 1
            #imageAfterScale = im
            #self.parent.canvas.data.imageAfterScale = im
        # imageWidth = canvas.data.image.size[0]
        # imageHeight = canvas.data.image.size[1]
        #imageAfterScaleWidth = self.parent.canvas.data.imageAfterScale.size[0]
        #imageAfterScaleHeight = self.parent.canvas.data.imageAfterScale.size[1]

        if (delta > 0):
            scaleRatio = scaleRatio * scaleUp
            #imageAfterScaleNew = imageAfterScale.resize(
                #(int(round(imageAfterScaleWidth * scaleUp)), int(round(imageAfterScaleHeight * scaleUp))))
        elif (delta < 0):
            scaleRatio = scaleRatio * scaleDown
            #imageAfterScaleNew = imageAfterScale.resize(
                #(int(round(imageAfterScaleWidth * scaleDown)), int(round(imageAfterScaleHeight * scaleDown))),
                #Image.ANTIALIAS)
        self.parent.canvas.data.scaleRatio = scaleRatio
        #imageAfterScaleNewWidth = imageAfterScaleNew.size[0]
        #imageAfterScaleNewHeight = imageAfterScaleNew.size[1]

        #imageAfterScale = im.resize((imageAfterScaleNewWidth, imageAfterScaleNewHeight))
        #self.parent.canvas.data.imageAfterScale = imageAfterScale
        #imageForTk = ImageTk.PhotoImage(imageAfterScale)


        #self.parent.canvas.create_image(self.parent.canvas.data.width / 2.0 - self.parent.canvas.data.resizedIm.size[0] / 2.0,
                            #self.parent.canvas.data.height / 2.0 - self.parent.canvas.data.resizedIm.size[1] / 2.0,
                            #anchor=NW, image=imageForTk)
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def mirror(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.mirror(self.parent.canvas.data.image)
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def flip(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.flip(self.parent.canvas.data.image)
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def brightness(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        self.parent.brightnessWindow = Toplevel(self.parent.canvas.data.mainWindow)
        self.parent.brightnessWindow.title("Brightness")
        self.parent.brightnessWindow.resizable(width=True, height=True)
        self.parent.brightnessWindow.geometry("200x90")
        self.parent.brightnessSlider = Scale(self.parent.brightnessWindow, from_=0, to=3, \
                                 length=150, tickinterval=1, resolution=0.5,
                                 orient=HORIZONTAL, command=self.updateBrightness)
        self.parent.brightnessSlider.set(self.parent.canvas.data.brightnessLevel)
        self.parent.brightnessSlider.pack()
        #self.updateBrightness()
        OkBrightnessFrame = Frame(self.parent.brightnessWindow)
        OkBrightnessButton = Button(OkBrightnessFrame, text="OK", \
                                    command=self.closeBrightnessWindow)
        OkBrightnessButton.grid(row=0, column=0)
        OkBrightnessFrame.pack(side=BOTTOM)
        #self.changeBrightness(brightnessWindow, brightnessSlider, self.parent.canvas.data.brightnessLevel)
        # brightnessSlider.set(0)

    def updateBrightness(self, value):
        brightnessLevel = self.parent.brightnessSlider.get()
        self.parent.canvas.data.brightnessLevel = brightnessLevel
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def changeBrightness(self, brightnessWindow, brightnessSlider, \
                         previousVal):
        if self.parent.canvas.data.brightnessWindowClose == True:
            brightnessWindow.destroy()
            self.parent.canvas.data.brightnessWindowClose = False

        else:
            # increasing pixel values according to slider value increases
            # brightness we change ot according to the difference between the
            # previous value and the current slider value
            if self.parent.canvas.data.image != None and brightnessWindow.winfo_exists():
                sliderVal = brightnessSlider.get()
                scale = (sliderVal - previousVal) / 100.0
                self.parent.canvas.data.image = self.parent.canvas.data.image.point( \
                    lambda i: i + int(round(i * scale)))
                self.parent.canvas.data.imageForTk = self.makeImageForTk()
                self.drawImage()
                self.parent.canvas.after(200, \
                             self.changeBrightness(brightnessWindow, \
                                                brightnessSlider, sliderVal))
                self.parent.canvas.data.brightnessLevel = sliderVal

    def closeBrightnessWindow(self):
        if self.parent.canvas.data.image != None:
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.brightnessWindowClose = True
            self.parent.brightnessWindow.destroy()

            brightness_converter = ImageEnhance.Brightness(self.parent.canvas.data.image)
            imageAfterBrightness = brightness_converter.enhance(self.parent.canvas.data.brightnessLevel)
            self.parent.canvas.data.image = imageAfterBrightness
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.brightnessLevel = 1


    ################ FILTER MENU FUNCTIONS ############################
    def xrange(self, x):
        return iter(range(x))

    def convertGray(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        #### The existing method to convert to a grayscale image converts the ####
        ####         image mode, so I used my own function to convert         ####
        # value of each channel of a pixel is set to the average of the original
        # values of the channels
        if self.parent.canvas.data.image != None:
            data = []
            for col in self.xrange(self.parent.canvas.data.image.size[1]):
                for row in self.xrange(self.parent.canvas.data.image.size[0]):
                    r, g, b = self.parent.canvas.data.image.getpixel((row, col))
                    avg = int(round((r + g + b) / 3.0))
                    R, G, B = avg, avg, avg
                    data.append((R, G, B))
            self.parent.canvas.data.image.putdata(data)
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def sepia(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        # this method first converts the image to B&W and then adds the
        # same amount of red and green to every pixel
        if self.parent.canvas.data.image != None:
            sepiaData = []
            aaa = self.parent.canvas.data.image.size[1]
            for col in self.xrange(self.parent.canvas.data.image.size[1]):
                for row in self.xrange(self.parent.canvas.data.image.size[0]):
                    r, g, b = self.parent.canvas.data.image.getpixel((row, col))
                    avg = int(round((r + g + b) / 3.0))
                    R, G, B = avg + 100, avg + 50, avg
                    sepiaData.append((R, G, B))
            self.parent.canvas.data.image.putdata(sepiaData)
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def invert(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.invert(self.parent.canvas.data.image)
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()


    ######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########
    def makeImageForTk(self):
        im = self.parent.canvas.data.image
        if self.parent.canvas.data.image != None:
            # Beacuse after cropping the now 'image' might have diffrent
            # dimensional ratios
            imageWidth = self.parent.canvas.data.image.size[0]
            imageHeight = self.parent.canvas.data.image.size[1]
            # To make biggest version of the image fit inside the canvas
            if imageWidth > imageHeight:
                resizedImage = im.resize((int(round(self.parent.canvas.data.width * self.parent.canvas.data.scaleRatio)), \
                                          int(round(float(imageHeight) * self.parent.canvas.data.width / imageWidth * self.parent.canvas.data.scaleRatio))), Image.ANTIALIAS)
                # store the scale so as to use it later
                self.parent.canvas.data.imageScale = float(imageWidth) / self.parent.canvas.data.width
            else:
                resizedImage = im.resize((int(round(float(imageWidth) * self.parent.canvas.data.height / imageHeight*self.parent.canvas.data.scaleRatio)), \
                                          int(round(self.parent.canvas.data.height * self.parent.canvas.data.scaleRatio))), Image.ANTIALIAS)
                #self.parent.canvas.data.imageScale = float(imageHeight) / self.parent.canvas.data.height
            # we may need to refer to ther resized image atttributes again
            brightness_converter = ImageEnhance.Brightness(resizedImage)
            imageAfterBrightness = brightness_converter.enhance(self.parent.canvas.data.brightnessLevel)

            self.parent.canvas.data.resizedIm = imageAfterBrightness
            return ImageTk.PhotoImage(imageAfterBrightness)

    def drawImage(self):
        if self.parent.canvas.data.image != None:
            # make the canvas center and the image center the same
            self.parent.canvas.delete("all")
            self.parent.canvas.create_image(self.parent.canvas.data.width / 2.0 - self.parent.canvas.data.resizedIm.size[0] / 2.0,
                                self.parent.canvas.data.height / 2.0 - self.parent.canvas.data.resizedIm.size[1] / 2.0,
                                anchor=NW, image=self.parent.canvas.data.imageForTk)
            self.parent.canvas.data.imageTopX = int(round(self.parent.canvas.data.width / 2.0 - self.parent.canvas.data.resizedIm.size[0] / 2.0))
            self.parent.canvas.data.imageTopY = int(round(self.parent.canvas.data.height / 2.0 - self.parent.canvas.data.resizedIm.size[1] / 2.0))

def main():
    root = Tk()
    app = Example(root)
    app.mainloop()

if __name__ == '__main__':
    main()