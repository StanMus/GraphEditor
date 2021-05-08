import tkinter
from tkinter import *
import random
from PIL import Image, ImageDraw, ImageTk, ImageOps

def keyPressed(canvas, event):
    if event.keysym == "z":
        undo(canvas)
    elif event.keysym == "y":
        redo(canvas)

def undo(canvas):
    a=3


def redo(canvas):
    a=4


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

def buttonsInit(root, canvas):
    a=2
def menuInit(root, canvas):
    a=1

def scale_image(canvas, delta):
    global resizedImage, im, imageForTk, imageAfterScale, imageAfterScaleNew
    scaleUp = 1.1
    scaleDown = 0.9
    im = canvas.data.image
    imageAfterScale = canvas.data.imageAfterScale
    if (canvas.data.imageAfterScale==None):
        imageAfterScale=im
        canvas.data.imageAfterScale=im
    imageWidth = canvas.data.image.size[0]
    imageHeight = canvas.data.image.size[1]
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

def init(root, canvas):
    buttonsInit(root, canvas)
    menuInit(root, canvas)
    #canvas.data.image = None
    canvas.data.imageAfterScale = None
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

    #canvas.data.undoQueue = deque([], 10)
    #canvas.data.redoQueue = deque([], 10)
    #canvas.pack()

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
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="gray")

    xsb = Scrollbar(root, orient="horizontal", command=canvas.xview)
    ysb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    canvas.configure(scrollregion=(0, 0, 850, 750))

    xsb.grid(row=1, column=0, sticky="ew")
    ysb.grid(row=0, column=1, sticky="ns")
    canvas.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    """
    # Plot some rectangles
    for n in range(2):
        x0 = random.randint(0, 900)
        y0 = random.randint(50, 900)
        x1 = x0 + random.randint(50, 100)
        y1 = y0 + random.randint(50, 100)
        color = ("red", "orange", "yellow", "green", "blue")[random.randint(0, 4)]
        canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill=color, activefill="black", tags=n)
    """

    File = '/Users/musolov.sn/Documents/GitHub/GraphEditor/picture.jpeg'
    im = Image.open(File)

    imageForTk = ImageTk.PhotoImage(im)
    canvas.create_image(0,
                        0,
                        anchor=NW, image=imageForTk)

    # This is what enables using the mouse:
    canvas.bind("<ButtonPress-1>", lambda event: move_start(canvas, event))
    canvas.bind("<B1-Motion>", lambda event: move_move(canvas, event))
    # windows scroll
    canvas.bind("<MouseWheel>", lambda event: zoomer(canvas, event))

    # Set up canvas data and call init
    class Struct: pass

    canvas.data = Struct()
    canvas.data.image = im
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.mainWindow = root
    init(root, canvas)
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits)



run()