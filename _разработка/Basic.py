# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk, ImageOps
import os
import ctypes
import imghdr
from collections import *

"""
CITATIONS
I found the command for changing the desktop background from this webpage:
http://stackoverflow.com/questions/14426475/change-wallpaper-in-python-for-user-while-being-system
"""


################ DRAW ################

def xrange(x):
    return iter(range(x))

def drawOnImage(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = True
    drawWindow = Toplevel(canvas.data.mainWindow)
    drawWindow.title = "Draw"
    drawFrame = Frame(drawWindow)
    redButton = Button(drawFrame, bg="red", width=2, \
                       command=lambda: colourChosen(drawWindow, canvas, "red"))
    redButton.grid(row=0, column=0)
    blueButton = Button(drawFrame, bg="blue", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "blue"))
    blueButton.grid(row=0, column=1)
    greenButton = Button(drawFrame, bg="green", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "green"))
    greenButton.grid(row=0, column=2)
    magentaButton = Button(drawFrame, bg="magenta", width=2, \
                           command=lambda: colourChosen(drawWindow, canvas, "magenta"))
    magentaButton.grid(row=1, column=0)
    cyanButton = Button(drawFrame, bg="cyan", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "cyan"))
    cyanButton.grid(row=1, column=1)
    yellowButton = Button(drawFrame, bg="yellow", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "yellow"))
    yellowButton.grid(row=1, column=2)
    orangeButton = Button(drawFrame, bg="orange", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "orange"))
    orangeButton.grid(row=2, column=0)
    purpleButton = Button(drawFrame, bg="purple", width=2, \
                          command=lambda: colourChosen(drawWindow, canvas, "purple"))
    purpleButton.grid(row=2, column=1)
    brownButton = Button(drawFrame, bg="brown", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "brown"))
    brownButton.grid(row=2, column=2)
    blackButton = Button(drawFrame, bg="black", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "black"))
    blackButton.grid(row=3, column=0)
    whiteButton = Button(drawFrame, bg="white", width=2, \
                         command=lambda: colourChosen(drawWindow, canvas, "white"))
    whiteButton.grid(row=3, column=1)
    grayButton = Button(drawFrame, bg="gray", width=2, \
                        command=lambda: colourChosen(drawWindow, canvas, "gray"))
    grayButton.grid(row=3, column=2)
    drawFrame.pack(side=BOTTOM)


def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image != None:
        canvas.data.drawColour = colour
        canvas.data.mainWindow.bind("<B1-Motion>", \
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()


def drawDraw(event, canvas):
    if canvas.data.drawOn == True:
        x = int(round((event.x - canvas.data.imageTopX) * canvas.data.imageScale))
        y = int(round((event.y - canvas.data.imageTopY) * canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=canvas.data.drawColour, \
                     outline=None)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


######################## FEATURES ###########################

def closeHistWindow(canvas):
    if canvas.data.image != None:
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.histWindowClose = True


def histogram(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    histWindow = Toplevel(canvas.data.mainWindow)
    histWindow.title("Histogram")
    canvas.data.histCanvasWidth = 350
    canvas.data.histCanvasHeight = 475
    histCanvas = Canvas(histWindow, width=canvas.data.histCanvasWidth, \
                        height=canvas.data.histCanvasHeight)
    histCanvas.pack()
    # provide sliders to the user to manipulate red, green and blue amounts in the image
    redSlider = Scale(histWindow, from_=-100, to=100, \
                      orient=HORIZONTAL, label="R")
    redSlider.pack()
    blueSlider = Scale(histWindow, from_=-100, to=100, \
                       orient=HORIZONTAL, label="B")
    blueSlider.pack()
    greenSlider = Scale(histWindow, from_=-100, to=100, \
                        orient=HORIZONTAL, label="G")
    greenSlider.pack()
    OkHistFrame = Frame(histWindow)
    OkHistButton = Button(OkHistFrame, text="OK", \
                          command=lambda: closeHistWindow(canvas))
    OkHistButton.grid(row=0, column=0)
    OkHistFrame.pack(side=BOTTOM)
    initialRGB = (0, 0, 0)
    changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, initialRGB)


def changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, previousRGB):
    if canvas.data.histWindowClose == True:
        histWindow.destroy()
        canvas.data.histWindowClose = False
    else:
        # the slider value indicates the % by which the red/green/blue
        # value of the pixels of the image need to incresed (for +ve values)
        # or decreased (for -ve values)
        if canvas.data.image != None and histWindow.winfo_exists():
            R, G, B = canvas.data.image.split()
            sliderValR = redSlider.get()
            (previousR, previousG, previousB) = previousRGB
            scaleR = (sliderValR - previousR) / 100.0
            R = R.point(lambda i: i + int(round(i * scaleR)))
            sliderValG = greenSlider.get()
            scaleG = (sliderValG - previousG) / 100.0
            G = G.point(lambda i: i + int(round(i * scaleG)))
            sliderValB = blueSlider.get()
            scaleB = (sliderValB - previousB) / 100.0
            B = B.point(lambda i: i + int(round(i * scaleB)))
            canvas.data.image = Image.merge(canvas.data.image.mode, (R, G, B))

            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
            displayHistogram(canvas, histWindow, histCanvas)
            previousRGB = (sliderValR, sliderValG, sliderValB)
            canvas.after(200, lambda: changeColours(canvas, redSlider, \
                                                    blueSlider, greenSlider, histWindow, histCanvas, previousRGB))


def displayHistogram(canvas, histWindow, histCanvas):
    histCanvasWidth = canvas.data.histCanvasWidth
    histCanvasHeight = canvas.data.histCanvasHeight
    margin = 50
    if canvas.data.image != None:
        histCanvas.delete(ALL)
        im = canvas.data.image
        # x-axis
        histCanvas.create_line(margin - 1, histCanvasHeight - margin + 1, \
                               margin - 1 + 258, histCanvasHeight - margin + 1)
        xmarkerStart = margin - 1
        for i in xrange(0, 257, 64):
            xmarker = "%d" % (i)
            histCanvas.create_text(xmarkerStart + i, \
                                   histCanvasHeight - margin + 7, text=xmarker)
        # y-axis
        histCanvas.create_line(margin - 1, \
                               histCanvasHeight - margin + 1, margin - 1, margin)
        ymarkerStart = histCanvasHeight - margin + 1
        for i in xrange(0, histCanvasHeight - 2 * margin + 1, 50):
            ymarker = "%d" % (i)
            histCanvas.create_text(margin - 1 - 10, \
                                   ymarkerStart - i, text=ymarker)

        R, G, B = im.histogram()[:256], im.histogram()[256:512], \
                  im.histogram()[512:768]
        for i in xrange(len(R)):
            pixelNo = R[i]
            histCanvas.create_oval(i + margin, \
                                   histCanvasHeight - pixelNo / 100.0 - 1 - margin, i + 2 + margin, \
                                   histCanvasHeight - pixelNo / 100.0 + 1 - margin, \
                                   fill="red", outline="red")
        for i in xrange(len(G)):
            pixelNo = G[i]
            histCanvas.create_oval(i + margin, \
                                   histCanvasHeight - pixelNo / 100.0 - 1 - margin, i + 2 + margin, \
                                   histCanvasHeight - pixelNo / 100.0 + 1 - margin, \
                                   fill="green", outline="green")
        for i in xrange(len(B)):
            pixelNo = B[i]
            histCanvas.create_oval(i + margin, \
                                   histCanvasHeight - pixelNo / 100.0 - 1 - margin, i + 2 + margin, \
                                   histCanvasHeight - pixelNo / 100.0 + 1 - margin, \
                                   fill="blue", outline="blue")


def colourPop(canvas):
    canvas.data.cropPopToHappen = False
    canvas.data.colourPopToHappen = True
    canvas.data.drawOn = False
    messagebox.showinfo(title="Colour Pop", message="Click on a part of the image which you want in colour",
                          parent=canvas.data.mainWindow)
    if canvas.data.cropPopToHappen == False:
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: getPixel(event, canvas))


def getPixel(event, canvas):
    # have to check if Colour Pop button is pressed or not, otherwise, the root
    # events which point to different functions based on what button has been
    # pressed will get mixed up
    try:  # to avoid confusion between the diffrent events
        # asscoaited with crop and colourPop
        if canvas.data.colourPopToHappen == True and \
                canvas.data.cropPopToHappen == False and canvas.data.image != None:
            data = []
            # catch the location of the pixel selected by the user
            # multiply it by the scale to get pixel's olaction of the
            # actual image
            canvas.data.pixelx = \
                int(round((event.x - canvas.data.imageTopX) * canvas.data.imageScale))
            canvas.data.pixely = \
                int(round((event.y - canvas.data.imageTopY) * canvas.data.imageScale))
            pixelr, pixelg, pixelb = \
                canvas.data.image.getpixel((canvas.data.pixelx, canvas.data.pixely))
            # the amount of deviation allowed from selected pixel's value
            tolerance = 60
            for y in xrange(canvas.data.image.size[1]):
                for x in xrange(canvas.data.image.size[0]):
                    r, g, b = canvas.data.image.getpixel((x, y))
                    avg = int(round((r + g + b) / 3.0))
                    # if the deviation of each pixel value > tolerance,
                    # make them gray else keep them coloured
                    if (abs(r - pixelr) > tolerance or
                            abs(g - pixelg) > tolerance or
                            abs(b - pixelb) > tolerance):
                        R, G, B = avg, avg, avg
                    else:
                        R, G, B = r, g, b
                    data.append((R, G, B))
            canvas.data.image.putdata(data)
            #save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
    except:
        pass
    canvas.data.colourPopToHappen = False


def crop(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.drawOn = False
    # have to check if crop button is pressed or not, otherwise,
    # the root events which point to
    # different functions based on what button has been pressed
    # will get mixed up
    canvas.data.cropPopToHappen = True
    messagebox.showinfo(title="Crop", \
                          message="Draw cropping rectangle and press Enter", \
                          parent=canvas.data.mainWindow)
    if canvas.data.image != None:
        canvas.data.mainWindow.bind("<ButtonPress-1>", \
                                    lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>", \
                                    lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", \
                                    lambda event: endCrop(event, canvas))


def startCrop(event, canvas):
    # detects the start of the crop rectangle
    if canvas.data.endCrop == False and canvas.data.cropPopToHappen == True:
        canvas.data.startCropX = event.x
        canvas.data.startCropY = event.y


def drawCrop(event, canvas):
    # keeps extending the crop rectange as the user extends
    # his desired crop rectangle
    if canvas.data.endCrop == False and canvas.data.cropPopToHappen == True:
        canvas.data.tempCropX = event.x
        canvas.data.tempCropY = event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                canvas.data.tempCropX, \
                                canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)


def endCrop(event, canvas):
    # set canvas.data.endCrop=True so that button pressed movements
    # are not caught anymore but set it to False when "Enter"
    # is pressed so that crop can be performed another time too
    if canvas.data.cropPopToHappen == True:
        canvas.data.endCrop = True
        canvas.data.endCropX = event.x
        canvas.data.endCropY = event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                canvas.data.endCropX, \
                                canvas.data.endCropY, fill="gray", stipple="gray12", width=0)
        canvas.data.mainWindow.bind("<Return>", \
                                    lambda event: performCrop(event, canvas))


def performCrop(event, canvas):
    canvas.data.image = \
        canvas.data.image.crop( \
            (int(round((canvas.data.startCropX - canvas.data.imageTopX) * canvas.data.imageScale)),
             int(round((canvas.data.startCropY - canvas.data.imageTopY) * canvas.data.imageScale)),
             int(round((canvas.data.endCropX - canvas.data.imageTopX) * canvas.data.imageScale)),
             int(round((canvas.data.endCropY - canvas.data.imageTopY) * canvas.data.imageScale))))
    canvas.data.endCrop = False
    canvas.data.cropPopToHappen = False
    #save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk = makeImageForTk(canvas)
    drawImage(canvas)


def rotateFinished(canvas, rotateWindow, rotateSlider, previousAngle):
    if canvas.data.rotateWindowClose == True:
        rotateWindow.destroy()
        canvas.data.rotateWindowClose = False
    else:
        if canvas.data.image != None and rotateWindow.winfo_exists():
            canvas.data.angleSelected = rotateSlider.get()
            if canvas.data.angleSelected != None and \
                    canvas.data.angleSelected != previousAngle:
                canvas.data.image = \
                    canvas.data.image.rotate(float(canvas.data.angleSelected))
                canvas.data.imageForTk = makeImageForTk(canvas)
                drawImage(canvas)
        canvas.after(200, lambda: rotateFinished(canvas, \
                                                 rotateWindow, rotateSlider, canvas.data.angleSelected))


def closeRotateWindow(canvas):
    if canvas.data.image != None:
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.rotateWindowClose = True


def rotate(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    rotateWindow = Toplevel(canvas.data.mainWindow)
    rotateWindow.title("Rotate")
    rotateSlider = Scale(rotateWindow, from_=0, to=360, orient=HORIZONTAL)
    rotateSlider.pack()
    OkRotateFrame = Frame(rotateWindow)
    OkRotateButton = Button(OkRotateFrame, text="OK", \
                            command=lambda: closeRotateWindow(canvas))
    OkRotateButton.grid(row=0, column=0)
    OkRotateFrame.pack(side=BOTTOM)
    rotateFinished(canvas, rotateWindow, rotateSlider, 0)


def closeBrightnessWindow(canvas):
    if canvas.data.image != None:
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose = True


def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose == True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose = False

    else:
        # increasing pixel values according to slider value increases
        # brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image != None and brightnessWindow.winfo_exists():
            sliderVal = brightnessSlider.get()
            scale = (sliderVal - previousVal) / 100.0
            canvas.data.image = canvas.data.image.point( \
                lambda i: i + int(round(i * scale)))
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200, \
                         lambda: changeBrightness(canvas, brightnessWindow, \
                                                  brightnessSlider, sliderVal))


def brightness(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    brightnessWindow = Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessWindow.resizable(width=True, height=True)
    brightnessWindow.geometry("200x90")
    brightnessSlider = Scale(brightnessWindow, from_=-100, to=100, \
                             orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame = Frame(brightnessWindow)
    OkBrightnessButton = Button(OkBrightnessFrame, text="OK", \
                                command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0, column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider, 0)
    #brightnessSlider.set(0)


def reset(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    ### change back to original image
    if canvas.data.image != None:
        canvas.data.image = canvas.data.originalImage.copy()
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def mirror(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.mirror(canvas.data.image)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def flip(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.flip(canvas.data.image)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def transpose(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    # I treated the image as a continuous list of pixel values row-wise
    # and simply excnaged the rows and the coloums
    # in oder to make it rotate clockewise, I reversed all the rows
    if canvas.data.image != None:
        imageData = list(canvas.data.image.getdata())
        newData = []
        newimg = Image.new(canvas.data.image.mode, \
                           (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in xrange(canvas.data.image.size[0]):
            addrow = []
            for j in xrange(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData += addrow
        newimg.putdata(newData)
        canvas.data.image = newimg.copy()
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


############### FILTERS ######################

def covertGray(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    #### The existing method to convert to a grayscale image converts the ####
    ####         image mode, so I used my own function to convert         ####
    # value of each channel of a pixel is set to the average of the original
    # values of the channels
    if canvas.data.image != None:
        data = []
        for col in xrange(canvas.data.image.size[1]):
            for row in xrange(canvas.data.image.size[0]):
                r, g, b = canvas.data.image.getpixel((row, col))
                avg = int(round((r + g + b) / 3.0))
                R, G, B = avg, avg, avg
                data.append((R, G, B))
        canvas.data.image.putdata(data)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def sepia(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    # this method first converts the image to B&W and then adds the
    # same amount of red and green to every pixel
    if canvas.data.image != None:
        sepiaData = []
        for col in xrange(canvas.data.image.size[1]):
            for row in xrange(canvas.data.image.size[0]):
                r, g, b = canvas.data.image.getpixel((row, col))
                avg = int(round((r + g + b) / 3.0))
                R, G, B = avg + 100, avg + 50, avg
                sepiaData.append((R, G, B))
        canvas.data.image.putdata(sepiaData)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def invert(canvas):
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.invert(canvas.data.image)
        #save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


################ EDIT MENU FUNCTIONS ############################

def keyPressed(canvas, event):
    if event.keysym == "z":
        undo(canvas)
    elif event.keysym == "y":
        redo(canvas)


# we use deques so as to make Undo and Redo more efficient and avoid
# memory space isuues
# after each change, we append the new version of the image to
# the Undo queue
def undo(canvas):
    if len(canvas.data.undoQueue) > 0:
        # the last element of the Undo Deque is the
        # current version of the image
        lastImage = canvas.data.undoQueue.pop()
        # we would want the current version if wehit redo after undo
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue) > 0:
        # the previous version of the image
        canvas.data.image = canvas.data.undoQueue[-1]
    #save(canvas)
    canvas.data.imageForTk = makeImageForTk(canvas)
    drawImage(canvas)


def redo(canvas):
    if len(canvas.data.redoQueue) > 0:
        canvas.data.image = canvas.data.redoQueue[0]
    #save(canvas)
    if len(canvas.data.redoQueue) > 0:
        # we remove this version from the Redo Deque beacuase it
        # has become our current image
        lastImage = canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk = makeImageForTk(canvas)
    drawImage(canvas)


############# MENU COMMANDS ################

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image != None:
        filename = filedialog.asksaveasfilename(defaultextension=".jpg")
        im = canvas.data.image
        im.save(filename)


def save(canvas):
    if canvas.data.image != None:
        im = canvas.data.image
        im.save(canvas.data.imageLocation)


def newImage(canvas):
    imageName = filedialog.askopenfilename(
            initialdir='/Users/musolov.sn/Documents/GitHub/GraphEditor',
            title='Выбрать файл',
            filetypes=(("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("gif files", "*.gif*"), ("png files", "*.png"))
    )
    filetype = ""
    # make sure it's an image file
    try:
        filetype = imghdr.what(imageName)
    except:
        messagebox.showinfo(title="Выбрать файл", \
                              message="Выберите файл-изображение!", parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff', 'jpg']:
        canvas.data.imageLocation = imageName
        im = Image.open(imageName)
        canvas.data.image = im
        canvas.data.originalImage = im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize = im.size  # Original Image dimensions
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)
    else:
        messagebox.showinfo(title="Выбрать файл", \
                              message="Выберите файл-изображение!", parent=canvas.data.mainWindow)

def onExit(root):
    root.quit()


######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im = canvas.data.image
    if canvas.data.image != None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
        imageWidth = canvas.data.image.size[0]
        imageHeight = canvas.data.image.size[1]
        # To make biggest version of the image fit inside the canvas
        if imageWidth > imageHeight:
            resizedImage = im.resize((canvas.data.width, \
                                      int(round(float(imageHeight) * canvas.data.width / imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale = float(imageWidth) / canvas.data.width
        else:
            resizedImage = im.resize((int(round(float(imageWidth) * canvas.data.height / imageHeight)), \
                                      canvas.data.height))
            canvas.data.imageScale = float(imageHeight) / canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm = resizedImage
        return ImageTk.PhotoImage(resizedImage)


def drawImage(canvas):
    if canvas.data.image != None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0,
                            canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX = int(round(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0))
        canvas.data.imageTopY = int(round(canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0))


############# DESKTOP BK ##############

## Please comment this function out if you use this on any OS apart from Windows

def desktopBk(canvas):
    if canvas.data.image != None:
        new = canvas.data.image.copy()
        # Windows desktop photos are supposed to be bitmap images
        newLocation = os.path.dirname( \
            canvas.data.imageLocation) + "/desktopPhoto.bmp"
        new.save(newLocation)
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, str(newLocation), 0)


############ INITIALIZE ##############

def init(root, canvas):
    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image = None
    canvas.data.imageAfterScale = None
    canvas.data.currentImage = None
    canvas.data.angleSelected = None
    canvas.data.rotateWindowClose = False
    canvas.data.brightnessWindowClose = False
    canvas.data.brightnessLevel = None
    canvas.data.histWindowClose = False
    canvas.data.solarizeWindowClose = False
    canvas.data.posterizeWindowClose = False
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.endCrop = False
    canvas.data.drawOn = True

    canvas.data.undoQueue = deque([], 10)
    canvas.data.redoQueue = deque([], 10)
    #canvas.pack()


def buttonsInit(root, canvas):
    backgroundColour = "white"
    buttonWidth = 14
    buttonHeight = 2
    toolKitFrame = Frame(root, name='frameTools')
    toolKitFrame.place(relx=0.85, rely=0,
                     relwidth=0.15, relheight=1)

    toolKitFrameInside = Frame(toolKitFrame)
    toolKitFrameInside.pack()

    cropButton = Button(toolKitFrameInside, text="Crop", \
                        background=backgroundColour, \
                        width=buttonWidth, height=buttonHeight, \
                        command=lambda: crop(canvas))
    cropButton.grid(row=0, column=0)
    rotateButton = Button(toolKitFrameInside, text="Rotate", \
                          background=backgroundColour, \
                          width=buttonWidth, height=buttonHeight, \
                          command=lambda: rotate(canvas))
    rotateButton.grid(row=1, column=0)
    brightnessButton = Button(toolKitFrameInside, text="Brightness", \
                              background=backgroundColour, \
                              width=buttonWidth, height=buttonHeight, \
                              command=lambda: brightness(canvas))
    brightnessButton.grid(row=2, column=0)
    histogramButton = Button(toolKitFrameInside, text="Histogram", \
                             background=backgroundColour, \
                             width=buttonWidth, height=buttonHeight, \
                             command=lambda: histogram(canvas))
    histogramButton.grid(row=3, column=0)
    colourPopButton = Button(toolKitFrameInside, text="Colour Pop", \
                             background=backgroundColour, \
                             width=buttonWidth, height=buttonHeight, \
                             command=lambda: colourPop(canvas))
    colourPopButton.grid(row=4, column=0)
    mirrorButton = Button(toolKitFrameInside, text="Mirror", \
                          background=backgroundColour, \
                          width=buttonWidth, height=buttonHeight, \
                          command=lambda: mirror(canvas))
    mirrorButton.grid(row=5, column=0)
    flipButton = Button(toolKitFrameInside, text="Flip", \
                        background=backgroundColour, \
                        width=buttonWidth, height=buttonHeight, \
                        command=lambda: flip(canvas))
    flipButton.grid(row=6, column=0)
    transposeButton = Button(toolKitFrameInside, text="Transpose", \
                             background=backgroundColour, width=buttonWidth, \
                             height=buttonHeight, command=lambda: transpose(canvas))
    transposeButton.grid(row=7, column=0)
    drawButton = Button(toolKitFrameInside, text="Draw", \
                        background=backgroundColour, width=buttonWidth, \
                        height=buttonHeight, command=lambda: drawOnImage(canvas))
    drawButton.grid(row=8, column=0)
    # Please comment this button out if you use this on any OS apart from Windows
    desktopButton = Button(toolKitFrameInside, text="Make Desktop Bk", \
                           background=backgroundColour, height=buttonHeight, \
                           width=buttonWidth, command=lambda: desktopBk(canvas))
    desktopButton.grid(row=9, column=0)
    #toolKitFrame.pack(side=LEFT)



def menuInit(root, canvas):
    menubar = Menu(root)

    # консоль Файл
    fileMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Файл", menu=fileMenu)
    fileMenu.add_command(label="Открыть", command=lambda: newImage(canvas))
    fileMenu.add_command(label="Сохранить", command=lambda: save(canvas))
    fileMenu.add_command(label="Сохранить как", command=lambda: saveAs(canvas))
    #fileMenu.add_command(label="Печать", command=lambda: onExit(root))
    #fileMenu.add_command(label="Экспорт", command=lambda: onExit(root))
    #fileMenu.add_command(label="Свойства", command=lambda: onExit(root))
    fileMenu.add_command(label="Выход", command=lambda: onExit(root))

    # консоль Правка
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Отменить действие", command=lambda: undo(canvas))
    editmenu.add_command(label="Выполнить действие", command=lambda: redo(canvas))
    editmenu.add_command(label="Отменить все", command = lambda: reset(canvas))
    menubar.add_cascade(label="Правка", menu=editmenu)
    root.config(menu=menubar)

    # консоль Формат
    formatMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Формат", menu=formatMenu)
    formatMenu.add_command(label="Увеличить")
    formatMenu.add_command(label="Уменьшить")
    formatMenu.add_command(label="Вращение", command=lambda: rotate(canvas))
    formatMenu.add_command(label="Отражение (горизонтально)", command=lambda: mirror(canvas))
    formatMenu.add_command(label="Отражение (вертикально)", command=lambda: flip(canvas))
    formatMenu.add_command(label="Коррекция яркости", command=lambda: brightness(canvas))
    formatMenu.add_command(label="Коррекция контрастности")
    formatMenu.add_command(label="Коррекция цветового баланса")

    # консоль Фильтры
    filtersMenu = Menu(formatMenu, tearoff=0)
    formatMenu.add_cascade(label="Фильтры", menu=filtersMenu)
    filtersMenu.add_command(label="Черно-белый", command=lambda: covertGray(canvas))
    filtersMenu.add_command(label="Инверсия", command=lambda: invert(canvas))
    filtersMenu.add_command(label="Размытие")
    filtersMenu.add_command(label="Обесцвечивание")
    filtersMenu.add_command(label="Сепия", command=lambda: sepia(canvas))
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

    root.config(menu=menubar)

#move
def move_start(canvas, event):
    canvas.scan_mark(event.x, event.y)
def move_move(canvas, event):
    canvas.scan_dragto(event.x, event.y, gain=1)

#windows zoom
def zoomer(canvas, event):
    if (event.delta > 0):
        canvas.scale("all", event.x, event.y, 1.1, 1.1)
    elif (event.delta < 0):
        canvas.scale("all", event.x, event.y, 0.9, 0.9)

    scale_image(canvas, event.delta)

    canvas.configure(scrollregion = canvas.bbox("all"))

def scale_image(canvas, delta):
    global resizedImage, im, imageForTk, imageAfterScale, imageAfterScaleNew
    scaleUp = 1.1
    scaleDown = 0.9
    im = canvas.data.image
    imageAfterScale = canvas.data.imageAfterScale
    if (imageAfterScale==None):
        imageAfterScale=im
        canvas.data.imageAfterScale=im
    #imageWidth = canvas.data.image.size[0]
    #imageHeight = canvas.data.image.size[1]
    imageAfterScaleWidth = canvas.data.imageAfterScale.size[0]
    imageAfterScaleHeight = canvas.data.imageAfterScale.size[1]

    if (delta > 0):
        imageAfterScaleNew = imageAfterScale.resize((int(round(imageAfterScaleWidth*scaleUp)), int(round(imageAfterScaleHeight*scaleUp))))
    elif (delta < 0):
        imageAfterScaleNew = imageAfterScale.resize((int(round(imageAfterScaleWidth * scaleDown)), int(round(imageAfterScaleHeight * scaleDown))), Image.ANTIALIAS)

    imageAfterScaleNewWidth = imageAfterScaleNew.size[0]
    imageAfterScaleNewHeight = imageAfterScaleNew.size[1]

    imageAfterScale = im.resize((imageAfterScaleNewWidth, imageAfterScaleNewHeight))
    canvas.data.imageAfterScale = imageAfterScale
    imageForTk = ImageTk.PhotoImage(imageAfterScale)
    canvas.delete("all")
    canvas.create_image(0,
                        0,
                        anchor=NW, image=imageForTk)

def run():
    # create the root and the canvas
    root = Tk()
    root.title("Графичекий редактор")
    root.iconbitmap('/Users/musolov.sn/Documents/GitHub/GraphEditor/icon.ico')
    root.resizable(width=True, height=True)
    root.geometry("1024x768")
    root.configure()  # Что значит?
    canvasWidth = 850
    canvasHeight = 750
    framePicture = Frame(root, name='framePicture')
    framePicture.place(x=0, y=0,
                       relwidth=0.85, relheight=1)
    canvas = Canvas(framePicture, width=canvasWidth, height=canvasHeight, \
                    background="gray")

    xsb = Scrollbar(framePicture, orient="horizontal", command=canvas.xview)
    ysb = Scrollbar(framePicture, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(0, 0, 850, 750))

    xsb.grid(row=1, column=0, sticky="ew")
    ysb.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")
    framePicture.grid_rowconfigure(0, weight=1)
    framePicture.grid_columnconfigure(0, weight=1)

    # This is what enables using the mouse:
    canvas.bind("<ButtonPress-1>", lambda event: move_start(canvas, event))
    canvas.bind("<B1-Motion>", lambda event: move_move(canvas, event))
    # windows scroll
    canvas.bind("<MouseWheel>", lambda event: zoomer(canvas, event))

    # Set up canvas data and call init
    class Struct: pass

    canvas.data = Struct()
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.mainWindow = framePicture
    init(root, canvas)
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits)


run()