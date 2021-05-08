from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageEnhance


class CustomImageEnhancer():
    def __init__(self):

        def onClickImport():
            askimage = filedialog.askopenfilename()
            self.img = Image.open(askimage)
            return self.img

        def converted_image(img_a, contrast, brightness, color, sharpness):
            contrast_converter = ImageEnhance.Contrast(img_a)
            img_b = contrast_converter.enhance(contrast)
            brightness_converter = ImageEnhance.Brightness(img_b)
            img_c = brightness_converter.enhance(brightness)
            color_converter = ImageEnhance.Color(img_c)
            img_d = color_converter.enhance(color)
            sharpness_converter = ImageEnhance.Sharpness(img_d)
            img_final = sharpness_converter.enhance(sharpness)
            return img_final

        def onClickDisplay():
            #cont = (ScalerContrast.get() + 10)/10
            bright = ScalerBrightness.get()
            #col = ScalerColor.get()
            #sharp = ScalerSharpness.get()
            img = self.img
            #new_img = converted_image(img, cont, bright, col, sharp)
            new_img = converted_image(img, bright)
            new_img.show()

        root = Tk()

        buttonsFrame = Frame(root, name='buttonsFrame')
        slidersFrame = Frame(root, name='slidersFrame')
        buttonsFrame.pack()
        slidersFrame.pack()

        OpenB = ttk.Button(buttonsFrame, text="Import Photo", command=onClickImport)
        OpenB.pack()
        DisplayButton=ttk.Button(buttonsFrame, text="Show", command=onClickDisplay)
        DisplayButton.pack()
        ScalerContrast= Scale(slidersFrame, from_=-100, to_=100, orient=HORIZONTAL)
        ScalerContrast.set(0)
        ScalerBrightness = Scale(slidersFrame, from_=-100, to_=100, orient=HORIZONTAL)
        ScalerColor = Scale(slidersFrame, from_=0, to_=100, orient=HORIZONTAL)
        ScalerSharpness = Scale(slidersFrame, from_=0, to_=100, orient=HORIZONTAL)

        ScalerContrast.grid(row=0, column=1)
        ScalerBrightness.grid(row=1, column=1)
        ScalerColor.grid(row=2, column=1)
        ScalerSharpness.grid(row=3, column=1)

        labelCon=Label(slidersFrame, text='Contrast')
        labelBr = Label(slidersFrame, text='Brightness')
        labelColor = Label(slidersFrame, text='Color')
        labelSharp = Label(slidersFrame, text='Sharpness')

        labelCon.grid(row=0, column=0)
        labelBr.grid(row=1, column=0)
        labelColor.grid(row=2, column=0)
        labelSharp.grid(row=3, column=0)

        root.mainloop()


window=CustomImageEnhancer()