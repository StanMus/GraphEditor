# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance
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
        self.parent.geometry("1366x1024")
        self.parent.configure()

        self.initMenubar()
        self.initCanvas()
        self.initFrameForButtons()

    def initMenubar(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # консоль Файл
        fileMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=fileMenu)
        fileMenu.add_command(label="Открыть...", command=self.newImage)
        fileMenu.add_command(label="Сохранить", command=self.save)
        fileMenu.add_command(label="Сохранить как", command=self.saveAs)
        fileMenu.add_command(label="Выход", command=self.onExit)

        # консоль Правка
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Отменить действие", command=self.undo)
        editmenu.add_command(label="Выполнить действие", command=self.redo)
        editmenu.add_command(label="Отменить все", command=self.reset)
        editmenu.add_separator()
        editmenu.add_command(label="Очистить холст", command=self.clearCanvas)
        menubar.add_cascade(label="Правка", menu=editmenu)

        # консоль Формат
        formatMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Формат", menu=formatMenu)
        formatMenu.add_command(label="Вращение", command=self.rotateImage)
        formatMenu.add_command(label="Вращение 90", command=self.rotate90Image)
        formatMenu.add_command(label="Отразить горизонтально", command=self.mirror)
        formatMenu.add_command(label="Отразить вертикально", command=self.flip)
        formatMenu.add_separator()
        formatMenu.add_command(label="Изменить яркость", command=self.changeBrightness)
        formatMenu.add_command(label="Изменить контрастность", command=self.changeContrast)
        formatMenu.add_command(label="Изменить цветовой баланс", command=self.changeColor)
        formatMenu.add_command(label="Изменить резкость", command=self.changeSharpness)

        # консоль Фильтры
        filtersMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Фильтры", menu=filtersMenu)
        filtersMenu.add_command(label="Черно-белый", command=self.blackAndWhite)
        filtersMenu.add_command(label="Инверсия", command=self.invert)
        filtersMenu.add_command(label="Сепия", command=self.sepia)
        filtersMenu.add_command(label="Автоконтрастность", command=self.autocontrast)
        filtersMenu.add_separator()
        filtersMenu.add_command(label="Оттенки красного", command=self.redChanel)
        filtersMenu.add_command(label="Оттенки зеленого", command=self.greenChanel)
        filtersMenu.add_command(label="Оттенки синего", command=self.blueChanel)
        filtersMenu.add_command(label="Оттенки серого", command=self.convertGray)

    def initFrameForButtons(self):
        backgroundColour = "white"
        buttonWidth = 20
        buttonHeight = 2
        toolKitFrame = Frame(self.parent, name='frameTools')
        toolKitFrame.place(relx=0.85, rely=0,
                           relwidth=0.15, relheight=1)

        labelFontStyle = ("Arial", 14)

        labelFormat = Label(toolKitFrame, text="Формат изображения:", bd=6)
        labelFormat.config(font=labelFontStyle)
        labelFormat.pack(pady=(8,0))
        toolKitFrameFormat = Frame(toolKitFrame)
        toolKitFrameFormat.pack()
        rotateImageButton = Button(toolKitFrameFormat, text="Вращение", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.rotateImage)
        rotateImageButton.grid(row=0, column=0)
        mirrorButton = Button(toolKitFrameFormat, text="Отразить горизонтально", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.mirror)
        mirrorButton.grid(row=1, column=0)
        flipButton = Button(toolKitFrameFormat, text="Отразить вертикально", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.flip)
        flipButton.grid(row=2, column=0)
        changeBrightnessButton = Button(toolKitFrameFormat, text="Изменить яркость", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.changeBrightness)
        changeBrightnessButton.grid(row=3, column=0, pady=(8,0))
        changeContrastButton = Button(toolKitFrameFormat, text="Изменить контрастность", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.changeContrast)
        changeContrastButton.grid(row=4, column=0)
        changeColorButton = Button(toolKitFrameFormat, text="Изменить цветовой баланс", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.changeColor)
        changeColorButton.grid(row=5, column=0)
        changeSharpnessButton = Button(toolKitFrameFormat, text="Изменить резкость", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.changeSharpness)
        changeSharpnessButton.grid(row=6, column=0)

        labelFilters = Label(toolKitFrame, text="Фильтры изображения:", bd=8)
        labelFilters.config(font=labelFontStyle)
        labelFilters.pack(pady=(15,0))

        toolKitFrameFilters = Frame(toolKitFrame)
        toolKitFrameFilters.pack()

        blackAndWhiteButton = Button(toolKitFrameFilters, text="Чёрно-белый", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.blackAndWhite)
        blackAndWhiteButton.grid(row=0, column=0)
        invertButton = Button(toolKitFrameFilters, text="Инверсия", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.invert)
        invertButton.grid(row=1, column=0)
        sepiaButton = Button(toolKitFrameFilters, text="Сепия", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.sepia)
        sepiaButton.grid(row=2, column=0)
        autocontrastButton = Button(toolKitFrameFilters, text="Автоконтрастность", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.autocontrast)
        autocontrastButton.grid(row=3, column=0)
        redChanelButton = Button(toolKitFrameFilters, text="Оттенки красного", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.redChanel)
        redChanelButton.grid(row=4, column=0, pady=(8,0))
        greenChanelButton = Button(toolKitFrameFilters, text="Оттенки зеленого", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.greenChanel)
        greenChanelButton.grid(row=5, column=0)
        blueChanelButton = Button(toolKitFrameFilters, text="Оттенки синего", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=self.blueChanel)
        blueChanelButton.grid(row=6, column=0)
        convertGrayButton = Button(toolKitFrameFilters, text="Оттенки серого", \
                                   background=backgroundColour, \
                                   width=buttonWidth, height=buttonHeight, \
                                   command=self.convertGray)
        convertGrayButton.grid(row=7, column=0)

    def initCanvas(self):
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
        self.parent.canvas.data.contrastWindowClose = False
        self.parent.canvas.data.colorWindowClose = False
        self.parent.canvas.data.sharpnessWindowClose = False
        self.parent.canvas.data.rotateLevel = 0
        self.parent.canvas.data.brightnessLevel = 1
        self.parent.canvas.data.contrastLevel = 1
        self.parent.canvas.data.colorLevel = 1
        self.parent.canvas.data.sharpnessLevel = 1
        self.parent.canvas.data.histWindowClose = False
        self.parent.canvas.data.solarizeWindowClose = False
        self.parent.canvas.data.posterizeWindowClose = False
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.endCrop = False
        self.parent.canvas.data.drawOn = True

        self.parent.canvas.data.undoQueue = deque([], 10)
        self.parent.canvas.data.redoQueue = deque([], 10)

    ################ FUNCTIONS ############################

    ################ FILE MENU FUNCTIONS ############################
    def newImage(self):
        imageName = filedialog.askopenfilename(
            initialdir='u/',
            title='Выбрать файл',
            filetypes=(
            ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("png files", "*.png"), ("bmp files", "*.bmp"), ("tiff files", "*.tiff"))
        )
        filetype = ""
        # make sure it's an image file
        try:
            filetype = imghdr.what(imageName)
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
        except:
            messagebox.showinfo(title="Выбрать файл", \
                                message="Выберите файл-изображение!", parent=self.parent.canvas.data.mainWindow)
    def save(self):
        if self.parent.canvas.data.image != None:
            im = self.parent.canvas.data.image
            im.save(self.parent.canvas.data.imageLocation)

    def saveAs(self):
        # ask where the user wants to save the file
        if self.parent.canvas.data.image != None:
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", title='Сохранить файл', filetypes=(
            ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("png files", "*.png"), ("bmp files", "*.bmp"), ("tiff files", "*.tiff"))
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

    def clearCanvas(self):
        self.parent.canvas.delete("all")

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

        if (delta > 0):
            scaleRatio = scaleRatio * scaleUp
        elif (delta < 0):
            scaleRatio = scaleRatio * scaleDown
        self.parent.canvas.data.scaleRatio = scaleRatio
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def mirror(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.mirror(self.parent.canvas.data.image)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def flip(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.flip(self.parent.canvas.data.image)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def rotateImage(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        self.parent.rotateWindow = Toplevel(self.parent.canvas.data.mainWindow)
        self.parent.rotateWindow.title("Вращение")
        self.parent.rotateWindow.resizable(width=True, height=True)
        self.parent.rotateWindow.geometry("200x90")
        self.parent.rotateSlider = Scale(self.parent.rotateWindow, from_=-90, to=90, \
                                            length=150, tickinterval=45, resolution=1,
                                            orient=HORIZONTAL, command=self.updateRotate)
        self.parent.rotateSlider.set(self.parent.canvas.data.rotateLevel)
        self.parent.rotateSlider.pack()
        OkRotateFrame = Frame(self.parent.rotateWindow)
        OkRotateButton = Button(OkRotateFrame, text="OK", \
                                   command=self.closeRotateWindow)
        OkRotateButton.grid(row=0, column=0)
        OkRotateFrame.pack(side=BOTTOM)

    def updateRotate(self, value):
        rotateLevel = self.parent.rotateSlider.get()
        self.parent.canvas.data.rotateLevel = rotateLevel
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def closeRotateWindow(self):
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.rotateWindowClose = True
            self.parent.rotateWindow.destroy()

            image = self.parent.canvas.data.image
            if (self.parent.canvas.data.rotateLevel >= 0):
                rotateLevel = self.parent.canvas.data.rotateLevel
            else:
                rotateLevel = 360 + self.parent.canvas.data.rotateLevel

            imageRotated = image.rotate(rotateLevel)  # degrees counter-clockwise

            self.parent.canvas.data.image = imageRotated
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.rotateLevel = 0

    def rotate90Image(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            image = self.parent.canvas.data.image
            self.parent.canvas.data.image = image.transpose(Image.ROTATE_90)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    ### Change Brightness ###
    def changeBrightness(self):
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
        OkBrightnessFrame = Frame(self.parent.brightnessWindow)
        OkBrightnessButton = Button(OkBrightnessFrame, text="OK", \
                                    command=self.closeBrightnessWindow)
        OkBrightnessButton.grid(row=0, column=0)
        OkBrightnessFrame.pack(side=BOTTOM)

    def updateBrightness(self, value):
        brightnessLevel = self.parent.brightnessSlider.get()
        self.parent.canvas.data.brightnessLevel = brightnessLevel
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def closeBrightnessWindow(self):
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.brightnessWindowClose = True
            self.parent.brightnessWindow.destroy()
            brightness_converter = ImageEnhance.Brightness(self.parent.canvas.data.image)
            imageAfterBrightness = brightness_converter.enhance(self.parent.canvas.data.brightnessLevel)
            self.parent.canvas.data.image = imageAfterBrightness
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.brightnessLevel = 1

    ### Change Contrast ###
    def changeContrast(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        self.parent.contrastWindow = Toplevel(self.parent.canvas.data.mainWindow)
        self.parent.contrastWindow.title("Contrast")
        self.parent.contrastWindow.resizable(width=True, height=True)
        self.parent.contrastWindow.geometry("200x90")
        self.parent.contrastSlider = Scale(self.parent.contrastWindow, from_=0, to=3, \
                                             length=150, tickinterval=1, resolution=0.5,
                                             orient=HORIZONTAL, command=self.updateContrast)
        self.parent.contrastSlider.set(self.parent.canvas.data.contrastLevel)
        self.parent.contrastSlider.pack()
        OkContrastFrame = Frame(self.parent.contrastWindow)
        OkContrastButton = Button(OkContrastFrame, text="OK", \
                                    command=self.closeContrastWindow)
        OkContrastButton.grid(row=0, column=0)
        OkContrastFrame.pack(side=BOTTOM)

    def updateContrast(self, value):
        contrastLevel = self.parent.contrastSlider.get()
        self.parent.canvas.data.contrastLevel = contrastLevel
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()


    def closeContrastWindow(self):
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.contrastWindowClose = True
            self.parent.contrastWindow.destroy()

            contrast_converter = ImageEnhance.Contrast(self.parent.canvas.data.image)
            imageAfterContrast = contrast_converter.enhance(self.parent.canvas.data.contrastLevel)
            self.parent.canvas.data.image = imageAfterContrast
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.contrastLevel = 1

    ### Change Color ###
    def changeColor(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        self.parent.colorWindow = Toplevel(self.parent.canvas.data.mainWindow)
        self.parent.colorWindow.title("Color")
        self.parent.colorWindow.resizable(width=True, height=True)
        self.parent.colorWindow.geometry("200x90")
        self.parent.colorSlider = Scale(self.parent.colorWindow, from_=0, to=3, \
                                           length=150, tickinterval=1, resolution=0.5,
                                           orient=HORIZONTAL, command=self.updateColor)
        self.parent.colorSlider.set(self.parent.canvas.data.colorLevel)
        self.parent.colorSlider.pack()
        OkColorFrame = Frame(self.parent.colorWindow)
        OkColorButton = Button(OkColorFrame, text="OK", \
                                  command=self.closeColorWindow)
        OkColorButton.grid(row=0, column=0)
        OkColorFrame.pack(side=BOTTOM)

    def updateColor(self, value):
        colorLevel = self.parent.colorSlider.get()
        self.parent.canvas.data.colorLevel = colorLevel
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def closeColorWindow(self):
        if self.parent.canvas.data.image != None:
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.colorWindowClose = True
            self.parent.colorWindow.destroy()

            color_converter = ImageEnhance.Color(self.parent.canvas.data.image)
            imageAfterColor = color_converter.enhance(self.parent.canvas.data.colorLevel)
            self.parent.canvas.data.image = imageAfterColor
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.colorLevel = 1

    ### Change Sharpness ###
    def changeSharpness(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        self.parent.sharpnessWindow = Toplevel(self.parent.canvas.data.mainWindow)
        self.parent.sharpnessWindow.title("Sharpness")
        self.parent.sharpnessWindow.resizable(width=True, height=True)
        self.parent.sharpnessWindow.geometry("200x90")
        self.parent.sharpnessSlider = Scale(self.parent.sharpnessWindow, from_=0, to=3, \
                                           length=150, tickinterval=1, resolution=0.5,
                                           orient=HORIZONTAL, command=self.updateSharpness)
        self.parent.sharpnessSlider.set(self.parent.canvas.data.sharpnessLevel)
        self.parent.sharpnessSlider.pack()
        OkSharpnessFrame = Frame(self.parent.sharpnessWindow)
        OkSharpnessButton = Button(OkSharpnessFrame, text="OK", \
                                  command=self.closeSharpnessWindow)
        OkSharpnessButton.grid(row=0, column=0)
        OkSharpnessFrame.pack(side=BOTTOM)

    def updateSharpness(self, value):
        sharpnessLevel = self.parent.sharpnessSlider.get()
        self.parent.canvas.data.sharpnessLevel = sharpnessLevel
        self.parent.canvas.data.imageForTk = self.makeImageForTk()
        self.drawImage()

    def closeSharpnessWindow(self):
        if self.parent.canvas.data.image != None:
            # save(canvas)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.sharpnessWindowClose = True
            self.parent.sharpnessWindow.destroy()

            sharpness_converter = ImageEnhance.Sharpness(self.parent.canvas.data.image)
            imageAfterSharpness = sharpness_converter.enhance(self.parent.canvas.data.sharpnessLevel)
            self.parent.canvas.data.image = imageAfterSharpness
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.sharpnessLevel = 1

    ################ FILTER MENU FUNCTIONS ############################
    def xrange(self, x):
        return iter(range(x))

    def blackAndWhite(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            image = self.parent.canvas.data.image
            imageBlackAndWhite = image.convert(mode='1', dither=False)
            # Split into 3 channels
            m = imageBlackAndWhite.split()[0]
            recombinedImage = m.convert('RGB')

            self.parent.canvas.data.image = recombinedImage

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
                    R, G, B = avg + 60, avg + 30, avg
                    sepiaData.append((R, G, B))
            self.parent.canvas.data.image.putdata(sepiaData)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def autocontrast(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.autocontrast(self.parent.canvas.data.image, cutoff = 2, ignore = 2)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def invert(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            self.parent.canvas.data.image = ImageOps.invert(self.parent.canvas.data.image)
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def redChanel(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            image = self.parent.canvas.data.image
            imageRGB = image.convert('RGB')
            # Split into 3 channels
            r, g, b = imageRGB.split()
            # Green to zero
            g = g.point(lambda i: i * 0)
            # Blue to zero
            b = b.point(lambda i: i * 0)
            # Recombine back to RGB image
            channeledImage = Image.merge('RGB', (r, g, b))

            self.parent.canvas.data.image = channeledImage
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def greenChanel(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            image = self.parent.canvas.data.image
            imageRGB = image.convert('RGB')
            # Split into 3 channels
            r, g, b = imageRGB.split()
            # Red to zero
            r = r.point(lambda i: i * 0)
            # Blue to zero
            b = b.point(lambda i: i * 0)
            # Recombine back to RGB image
            channeledImage = Image.merge('RGB', (r, g, b))

            self.parent.canvas.data.image = channeledImage
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

    def blueChanel(self):
        self.parent.canvas.data.colourPopToHappen = False
        self.parent.canvas.data.cropPopToHappen = False
        self.parent.canvas.data.drawOn = False
        if self.parent.canvas.data.image != None:
            image = self.parent.canvas.data.image
            imageRGB = image.convert('RGB')
            # Split into 3 channels
            r, g, b = imageRGB.split()
            # Red to zero
            r = r.point(lambda i: i * 0)
            # Green to zero
            g = g.point(lambda i: i * 0)
            # Recombine back to RGB image
            channeledImage = Image.merge('RGB', (r, g, b))

            self.parent.canvas.data.image = channeledImage
            self.parent.canvas.data.undoQueue.append(self.parent.canvas.data.image.copy())
            self.parent.canvas.data.imageForTk = self.makeImageForTk()
            self.drawImage()

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
            # we may need to refer to ther resized image atttributes again



            #Apply filters Brightness, Contrast, Color, Sharpness
            brightness_converter = ImageEnhance.Brightness(resizedImage)
            imageAfterBrightness = brightness_converter.enhance(self.parent.canvas.data.brightnessLevel)

            contrast_converter = ImageEnhance.Contrast(imageAfterBrightness)
            imageAfterContrast = contrast_converter.enhance(self.parent.canvas.data.contrastLevel)

            color_converter = ImageEnhance.Color(imageAfterContrast)
            imageAfterColor = color_converter.enhance(self.parent.canvas.data.colorLevel)

            sharpness_converter = ImageEnhance.Sharpness(imageAfterColor)
            imageAfterSharpness = sharpness_converter.enhance(self.parent.canvas.data.sharpnessLevel)

            imageRotated = imageAfterSharpness.rotate(self.parent.canvas.data.rotateLevel)

            imageAfterAllFilters = imageRotated

            self.parent.canvas.data.resizedIm = imageAfterAllFilters
            return ImageTk.PhotoImage(imageAfterAllFilters)

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