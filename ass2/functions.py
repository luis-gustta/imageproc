### functions ###

## importing libraries ##
from typing import Union
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import numpy as np
import matplotlib.pyplot as plt

## tkinter constants ##
from tkinter import TOP
from tkinter import BOTH

## aux. modules to display plt plots on tkinter windows ##
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


window = Tk() # creating a top-level window called window
grayscale_state = 0 # global variable used to determine the grayscale state of the image

## creating the variables for the other windows ##
new_window1 = Toplevel(window)
new_window1.destroy()

new_window2 = Toplevel(window)
new_window2.destroy()

load_img_var = 0 # global variable used to determine if an image is loaded

## progressbar ##
pb = ttk.Progressbar(window, orient=HORIZONTAL, length=180, mode='determinate')
pb.place(x=97, y=305)

Label(window, text="Progress:").place(x=15, y=304)

## beginning of the functions ##
def open_img_file():
    '''
    ## open_img_file()
    Opens an image file, assigning it to an global variable called `img`,
    and the respective extension to another global variable caled `extension`.
    '''
    # defining the global variables #
    global new_window
    global extension
    global img
    global load_img_var

    try: # close all image windows before opening another
        destroy_all()
        open_img_file()
    except:
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(
        ), title="Select file", filetypes=(("image files", ".png .jpg .bmp .jpeg .tif . tiff"), ("jpg images", ".jpg"), ("png images", ".png"), ("all files", "*.*")))
        if not filename:
        	return
	    
        # setup new_window #
        new_window = Toplevel(window)
        new_window.title('Original Image')
        new_window.geometry("+330+220")
        
        img = Image.open(filename) # open image
        image = ImageTk.PhotoImage(img) # displays the image in tkinter window
        panel = Label(new_window, image=image)
        panel.image = image
        panel.pack()
        extension = os.path.splitext(filename)[1] # get extension
        load_img_var = 1

def IsLoaded():
    '''
    ## IsLoaded()
    Tests if the image is loaded or not. Ask the user to open the image if necessary.
    '''
    if load_img_var != 1:
        a = messagebox.askyesno("Error", "No image has been loaded!\nWant to open an image file?")
        if a == True:
            open_img_file()
            return
        else:
            pass

def save_img_file():
    '''
    ## save_img_file()
    Saves an image file, from an stored image in the gobal variable called `img`,
    using the respective extension from the global variable caled `extension`.
    '''
    IsLoaded() # check if the image is loaded
    save_filename = filedialog.asksaveasfile(mode='wb', initialfile = f'new_image{extension}',
    title="Save As", defaultextension=extension, filetypes=((f"{extension.replace('.','')} images",
    extension), ("all files", "*.*")))
    img.save(save_filename)

def copy(r=0):
    '''
    ## copy()
    Updates the `img` variable and display in tkinter window. The `img` variable is not modified.
    '''
    global new_window1

    new_window1.destroy()

    width, height = img.size
    new_window1 = Toplevel(window)
    new_window1.geometry(f"+{335+width+r}+220")
    new_window1.title('Edited Image')
    
    im = ImageTk.PhotoImage(img)
    panel1 = Label(new_window1, image=im)
    panel1.image = im
    panel1.pack()

def copy_n():
    '''
    ## copy_n()
    Updates the `img` variable and display in tkinter window. The `img` variable 
    is turned to the original image.
    '''
    IsLoaded() # check if the image is loaded
    global new_window1
    global img
    global state
    global grayscale_state
    global rot_var
    grayscale_state = 0
    try:
        new_window2.destroy()
    except:
        pass
    try:
        os.remove(f'{filename}_curr.jpg') # grants that quantize func. don't get an b&w saved pic.
    except:
        pass
    img = Image.open(filename)

    new_window1.destroy()

    width, height = img.size
    new_window1 = Toplevel(window)
    new_window1.geometry(f"+{335+width}+220")
    new_window.title('Original Image')
    new_window1.title('Original Image (copy)')
    
    im = ImageTk.PhotoImage(img)
    panel1 = Label(new_window1, image=im)
    panel1.image = im
    panel1.pack()
    state = 0
    rot_var = 0

def flip_loop(): # version with loop
    '''
    ## flip_loop()
    Flips an image called `img`, using multiple loops, update it's value and displays 
    the updated image.
    '''
    IsLoaded() # check if the image is loaded
    global img
    k = option.get()
    width, height = img.size
    if k == 2: # vertical
        for x in range(width): # over columns
            for y in range(height // 2): # over rows
                up = img.getpixel((x, y))
                down = img.getpixel((x, height - 1 - y))
                img.putpixel((x, height - 1 - y), up)
                img.putpixel((x, y), down)
            window.update_idletasks() # update window to update progressbar
            pb['value'] = x/width*100 # set progressbar value
        pb['value'] = 0 # when the loop finishes, set the value to 0
    elif k == 1: # horizontal
        for y in range(height): # over rows 
            for x in range(width // 2): # over columns
                left = img.getpixel((x, y))
                right = img.getpixel((width - 1 - x, y))
                img.putpixel((width - 1 - x, y), left)
                img.putpixel((x, y), right)
            window.update_idletasks() # update window to update progressbar
            pb['value'] = y/height*100 # set progressbar value
        pb['value'] = 0 # when the loop finishes, set the value to 0
    else:
        return
    new_window1.destroy()
    copy()

def flip(): # version with Numpy
    '''
    ## flip
    Flips an image called `img`, using Numpy methods, update it's value and displays the updated image.
    '''
    IsLoaded() # check if the image is loaded
    global img
    k = option.get()
    if k == 2:
        img_aux = np.array(img) # read as npArray
        img = Image.fromarray(np.flipud(img_aux)) # define the new flipped image
    elif k == 1:
        img_aux = np.array(img) # read as npArray
        img = Image.fromarray(np.fliplr(img_aux)) # define the new flipped image
    else:
        return
    new_window1.destroy()
    copy()

def grayscale_loop(): # version with loops
    '''
    ## grayscale_loop()
    Turns an image called `img`, using multiple loops, to grayscale and displays the updated image.
    '''
    IsLoaded() # check if the image is loaded
    global img
    global grayscale_state
    global pb
    grayscale_state = 1
    width, height = img.size
    r, g, b = [0.299, 0.587, 0.114] # rgb weights for grayscale
    pixels = img.load()
    
    for i in range(width):
        for j in range(height):
            # getting the RGB pixel value.
            pix = img.getpixel((i, j))
            # Apply formula of grayscale:
            element = int(r*pix[0] + g*pix[1] + b*pix[2])
            # setting the pixel value.
            pixels[i, j] = (element, element, element)
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/height*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    new_window1.destroy()
    copy()

def grayscale(): # version with matrix dot product by Numpy
    '''
    ## grayscale()
    Turns an image called `img`, using Numpy methods, to grayscale and displays the updated image.
    '''
    IsLoaded() # check if the image is loaded
    global img
    global grayscale_state
    grayscale_state = 1
    try:
        img_aux = np.array(img) # read as npArray
    except:
        copy_n()
    rgb_weights = [0.299, 0.587, 0.114] # rgb weights for grayscale
    img = Image.fromarray(np.dot(img_aux[...,:3], rgb_weights)) # define new grayscale image
    new_window1.destroy()
    copy()

state = 0   # create a variable used to track the saving of the image

def quantize(): # version with Numpy
    '''
    ## quantize()
    Quantize an image called `img`, using Numpy methods, to the specified values of 
    `quant_var` and displays the updated image.
    '''
    IsLoaded() # check if the image is loaded
    global img
    global state
    global grayscale_state
    try:
        img_aux = np.array(Image.open(f'{filename}_curr.jpg')) # read as npArray
    except:
        img_aux = np.array(img)
    if state == 0:
        img.save(f'{filename}_curr.jpg') # creates a temporary file (should have used time based name!)
        state = 1
    tones = int(quant_var.get())
    if tones > 255:
        return
    ratio = 255/tones  # Set quantization ratio
    if grayscale_state == 1: # if grayscale = True
        for i in range(img_aux.shape[0]): # for each row
            for j in range(img_aux.shape[1]): # for each column
                el = int(img_aux[i][j][0]/ratio)*ratio # for each pixel
                img_aux[i][j] = (el, el, el) # luma
            window.update_idletasks() # update window to update progressbar
            pb['value'] = i/img_aux.shape[0]*100 # set progressbar value
        pb['value'] = 0 # when the loop finishes, set the value to 0
    else:                    # if grayscale != True
        for i in range(img_aux.shape[0]): # for each row
            for j in range(img_aux.shape[1]): # for each column
                for k in range(img_aux.shape[2]): # for each pixel value
                    img_aux[i][j][k] = int(img_aux[i][j][k]/ratio)*ratio # each color
            window.update_idletasks() # update window to update progressbar
            pb['value'] = i/img_aux.shape[0]*100 # set progressbar value
        pb['value'] = 0 # when the loop finishes, set the value to 0
    img = Image.fromarray(img_aux)
    copy()

def quantizeWInteval(): # version with loops
    '''
    ## quantizeWInterval()
    Quantize an image called `img`, using multiple loops, to the specified values of 
    `quant_var` and displays the updated image.
    '''
    IsLoaded() # check if the image is loaded
    global grayscale_state
    global img
    global state
    global pb
    a_arr = []
    try:
        img_aux = np.array(Image.open(f'{filename}_curr.jpg')) # read as npArray if the saved aux_img exists
    except:
        img_aux = np.array(img) # if not, uses the current img
    if state == 0:
        img.save(f'{filename}_curr.jpg') # save the image after each application
        state = 1
    tones = int(quant_var.get()) # get the desired final tones by the quant_var global variable
    #print(img_aux)
    rgb1, rgb2 = img_aux.min(axis=1), img_aux.max(axis=1)
    t1, t2 = rgb1.min(axis=0), rgb2.max(axis=0)
    tam_int_r = (t2[0] - t1[0] + 1)
    tam_int_g = (t2[1] - t1[1] + 1)
    tam_int_b = (t2[2] - t1[2] + 1)
    #if tones >= tam_int_r and tones >= tam_int_r and tones >= tam_int_b:
    #    return
    tbr = tam_int_r/tones
    tbg = tam_int_g/tones
    tbb = tam_int_b/tones
    print(f'minR: {t1[0]}, maxR: {t2[0]}') # min_max before remap
    print(f'minG: {t1[1]}, maxG: {t2[1]}') # min_max before remap
    print(f'minB: {t1[2]}, maxB: {t2[2]}') # min_max before remap
    intervals = np.zeros((3, tones, 2))
    ar, ag, ab = t1[0]-0.5, t1[2]-0.5, t1[1]-0.5
    br, bg, bb = t1[1]-0.5, t1[0]-0.5, t1[2]-0.5
    i = 1
    if grayscale_state == 1: # if the image is grayscale
        tones = int(quant_var.get())
        t1, t2 = img_aux.min(), img_aux.max()
        tam_int = (t2 - t1 + 1)
        if tones >= tam_int:
            return
        tb = tam_int/tones
        print(f'min: {t1}, max: {t2}') # min_max before remap
        intervals = []
        a = t1-0.5
        b = t1-0.5
        i = 1
        for i in range(tones):
            intervals.append((int(a), int(b+i*tb)))
            a = int(b+i*tb)
            i += 1
        for i in range(img_aux.shape[0]): # iterates over lines
            for j in range(img_aux.shape[1]): # iterates over colums
                #for k in range(img_aux.shape[2]): # iterates over pixel values
                for g in intervals: # grayscale
                    if g[0] <= img_aux[i][j][0] <= g[1]:   # r
                        el = int((g[0]+g[1])/2)
                        if el < 0:
                            el = 0
                        #el = el-50# if el-150/tones >= 0 else el
                        img_aux[i][j] = (el, el, el) # turns to gray
                    else:
                        continue
            window.update_idletasks() # update window to update progressbar
            pb['value'] = i/img_aux.shape[0]*100 # set progressbar value
        pb['value'] = 0 # when the loop finishes, set the value to 0            
        img = Image.fromarray(img_aux)
        copy()
        return
    for i in range(tones): # if not grayscale
        intervals[0][i][0]=int(ar)
        intervals[0][i][1]=int(br+i*tbr)
        ar = int(br+i*tbr)

        intervals[1][i][0]=int(ag)
        intervals[1][i][1]=int(bg+i*tbg)
        ag = int(bg+i*tbg)

        intervals[2][i][0]=int(ab)
        intervals[2][i][1]=int(bb+i*tbb)
        ab = int(bb+i*tbb)
        i += 1
    #print(intervals)
    for i in range(img_aux.shape[0]): # iterates over lines
        for j in range(img_aux.shape[1]): # iterates over colums
            #for k in range(img_aux.shape[2]): # iterates over pixel values
            for g in intervals[0]:
                if g[0] <= img_aux[i][j][0] <= g[1]:   # r
                    el = int((g[0]+g[1])/2)
                    if el < 0:
                        el = 0
                    img_aux[i][j][0] = el # pixel value [0] = r
                else:
                    continue
            for g in intervals[1]:
                if g[0] <= img_aux[i][j][1] <= g[1]:   # g
                    el = int((g[0]+g[1])/2)
                    if el < 0:
                        el = 0
                    img_aux[i][j][1] = el # pixel value [1] = g
                else:
                    continue
            for g in intervals[2]:
                if g[0] <= img_aux[i][j][2] <= g[1]:   # b
                    el = int((g[0]+g[1])/2)
                    if el < 0:
                        el = 0
                    #print(el)
                    img_aux[i][j][2] = el # pixel value [2] = b
                else:
                    continue
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/img_aux.shape[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    img = Image.fromarray(img_aux)
    grayscale_state = 0
    copy()

#### new functions ####
def truncate(n: Union[int, float]) -> int:
    '''
    ## Truncate
    Returns the corrected value of a number `n`, in the range 0 to 255.

    Parameters
    ----------
    n : int | float
        Variable to be truncated
    '''
    return 0 if n < 0 else 255 if n > 255 else int(n)

def brightAdjust():
    '''
    ## brightAdjust()
    Change the brightness of an image called `img` by the specified values of `bright_var`
    and displays the updated image. Uses the variable `factor_state`, to determine if the
    given value must be used as a plain number or as a factor.
    '''
    IsLoaded() # check if the image is loaded
    brightness = int(bright_var.get()) # get the brightness from the variable
    factor = factor_state.get() # get the factor from the variable
    
    if factor == 1: # if factor is 1, then brightness is a factor in the range 0 to 255
        aux_brightness = (259 * (brightness+255)) / (255 * (259-brightness))
    else: # if factor is not 1, then brightness is the raw number in the range 0 to 255
        aux_brightness = brightness

    for x in range(img.size[0]): # over columns
        for y in range(img.size[1]): # over rows
            color = img.getpixel((x, y)) # get the current color
            new_color = tuple(truncate(aux_brightness + c) for c in color) # define the new color
            img.putpixel((x, y), new_color) # write the new pixel to the image
        window.update_idletasks() # update window to update progressbar
        pb['value'] = x/img.size[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    copy()

def contAdjust():
    '''
    ## contAdjust()
    Change the contrast of an image called `img` by the specified values of `cont_var`
    and displays the updated image. Uses the variable `factor_state`, to determine if the
    given value must be used as a plain number or as a factor.
    '''
    IsLoaded() # check if the image is loaded
    contrast = int(cont_var.get()) # get the contrast from the variable
    factor = factor_state.get() # get the factor from the variable

    if factor == 1: # if factor is 1, then contrast is a factor in the range 0 to 255
        aux_contrast = (259 * (contrast+255)) / (255 * (259-contrast))
    else: # if factor is not 1, then contrast is the raw number in the range 0 to 255
        aux_contrast = contrast

    for x in range(img.size[0]): # over columns
        for y in range(img.size[1]): # over rows
            color = img.getpixel((x, y)) # get the current color
            new_color = tuple(truncate(aux_contrast *(c-128) + 128) for c in color) # define the new color
            img.putpixel((x, y), new_color) # write the new pixel to the image
        window.update_idletasks() # update window to update progressbar
        pb['value'] = x/img.size[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    copy()

def invert():
    '''
    ## invert()
    Invert the colors of an image called `img`.
    '''
    IsLoaded() # check if the image is loaded

    for x in range(img.size[0]): # over columns
        for y in range(img.size[1]): # over rows
            color = img.getpixel((x, y)) # get the current color
            new_color = tuple(truncate(255 - c) for c in color) # define the new color
            img.putpixel((x, y), new_color) # write the new pixel to the image
        window.update_idletasks() # update window to update progressbar
        pb['value'] = x/img.size[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    copy()

def calcHistogram(a=0, b: Union[int, float] =30, title: str ='Histogram', only_histo=1) -> np.ndarray:
    '''
    ## CalcHistogram()
    Calculates the histogram of an image `img` and returns the histogram.

    Parameters
    ----------
    a : any, optional
        Auxiliary variable to determine if such a window exists

    b : int | float, optional
        The amount of vaiation in the position of window

    title : str, optional
        The title of the created window (default is 'Histogram')
    
    only_histo : any, optional
        Determines if the function will only calculate the histogram or not, if equal to 1 
        generate also RGB histograms
    '''
    IsLoaded() # check if the image is loaded
    global new_window2
    try:
        for widget in new_window2.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
    except:
        pass
    if a == 0:
        new_window2.destroy()
    if only_histo == 1 and grayscale_state != 1:
        width, height = img.size
        img_aux = np.array(img)

        # initialize an array of 256 ints (all zero)
        # the index range for this list is [0, 255]
        histogramR = np.zeros([256], np.int32) # red channel
        histogramG = np.zeros([256], np.int32) # green channel
        histogramB = np.zeros([256], np.int32) # blue channel
        
        # loop through each pixel in image
        for y in range(0, height):
            for x in range(0, width):
                histogramR[img_aux[y, x, 0]] +=1 # red channel
                histogramG[img_aux[y, x, 1]] +=1 # green channel
                histogramB[img_aux[y, x, 2]] +=1 # blue channel
            window.update_idletasks() # update window to update progressbar
            pb['value'] = y/height*100 # set progressbar value
        pb['value'] = 0 # when the loop finishes, set the value to 0
        
        new_window2 = Toplevel(window)
        new_window2.wm_title(title)
        new_window2.geometry('280x170')
        new_window2.geometry(f'+{b}+0')

        ## plot parameters ##
        plt.rcParams.update({'font.size': 8})
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        ## Red channel ##
        ax.plot(np.arange(0,256,1), histogramR/max(histogramR), color='red', linewidth='0')
        ax.fill_between(np.arange(0,256,1), histogramG/max(histogramR), alpha=0.4, color='red')
        
        ## Blue channel ##
        ax.plot(np.arange(0,256,1), histogramG/max(histogramG), color='green', linewidth='0')
        ax.fill_between(np.arange(0,256,1), histogramR/max(histogramR), alpha=0.4, color='green')

        ## Green channel ##
        ax.plot(np.arange(0,256,1), histogramB/max(histogramB), color='blue', linewidth='0')
        ax.fill_between(np.arange(0,256,1), histogramB/max(histogramB), alpha=0.4, color='blue')
        
        ## plot limits ##
        ax.set_xlim([0,255])
        ax.set_ylim([0,1])

        ## display the plot in Tkinter env. ##
        canvas = FigureCanvasTkAgg(fig, master=new_window2)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, new_window2)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        return(histogramR, histogramG, histogramB)
        
    #if grayscale_state != 1:
    #    grayscale_loop()
    width, height = img.size
    img_aux = np.array(img)

    histogram = np.zeros([256], np.int32) # index range --> [0, 255]
    
    # loop through each pixel in image
    for y in range(0, height):
        for x in range(0, width):
            histogram[img_aux[y, x]] +=1
        window.update_idletasks() # update window to update progressbar
        pb['value'] = y/height*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    #plt.xlim([0,255])
    #plt.ylim([0,1])
    #plt.show()

    new_window2 = Toplevel(window)
    new_window2.wm_title(title)
    new_window2.geometry('280x170')
    new_window2.geometry(f'+{b}+0')

    ## plot parameters ##
    plt.rcParams.update({'font.size': 8})
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    ## grayscale histogram plot ##
    ax.plot(np.arange(0,256,1), histogram/max(histogram), color='black', linewidth='0')
    ax.fill_between(np.arange(0,256,1), histogram/max(histogram), alpha=0.4, color='black')

    ## plot limits ##
    ax.set_xlim([0,255])
    ax.set_ylim([0,1])

    ## displays the plot in Tkinter env. ##
    canvas = FigureCanvasTkAgg(fig, master=new_window2)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, new_window2)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    return(histogram)

def destroy_all():
    '''
    ## destroy_all()
    Close all TopLevel-windows created on top of the window widget.
    '''
    for widget in window.winfo_children(): # over the children of window
        if isinstance(widget, Toplevel): # if is Toplevel window, then destroy
            widget.destroy()

def histogramQuant(a=0, b=0):
    '''
    ## histogramQuant()
    Quantize an image called `img` or `img2` based on the value of the argument `a`.

    Parameters
    ----------
    a : any, optional
        Auxiliary variable to determine if the image to be quantized is the current image (`img`)
        or the image to be matched by histogram matching (`img2`)
    '''
    IsLoaded() # check if the image is loaded
    global img
    try:
        for widget in new_window2.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()
        new_window2.destroy()
    except:
        pass
    ## determine the image to be used ##
    if a == 0:
        img = img
    else:
        save_img = img
        img = img2
    def cumsum(arr): # calculate the cumulative sum
        arr = iter(arr)
        b = [next(arr)]
        for i in arr:
            b.append(b[-1] + i)
        return np.array(b)
    
    c_sum = cumsum(calcHistogram(only_histo=0)) # calculate the cumulative sum of the histogram
    img_aux = np.asarray(img) # create an auxiliary image np.array
    flat = img_aux.flatten() # flatten the image to 1D array
    
    nj = (c_sum - c_sum.min()) * 255
    N = c_sum.max() - c_sum.min()

    # re-normalize the cumulative distribution function
    c_sum = nj / N
    c_sum = convert(c_sum)# same as "c_sum.astype('uint8')", convert the values to uint8
    img_aux = np.reshape(c_sum[flat], img_aux.shape) # reshape the 1D array to the image array
    img = Image.fromarray(img_aux)
    if a != 0 and b != 0:
        calcHistogram(a=1, b=320, title='Quantized Histogram', only_histo=0)
    else:
        calcHistogram(a=1, b=320, title='Quantized Histogram', only_histo=0)
    try:
        img = save_img
    except:
        pass
    copy()

def getKernel(kernel:str) -> np.ndarray:
    '''
    ## getKernel()
    Returns a kernel defined by the given kernel name.

    Parameters
    ----------
    kernel : str
        Kernel to be returned as a numpy ndarray
    '''
    kernels = {'Gaussian':np.array([[0.0625, 0.125, 0.0625], 
                                      [0.1250, 0.250, 0.1250], 
                                      [0.0625, 0.125, 0.0625]]), 
               'Laplacian':np.array([[0, -1,  0], 
                                       [-1, 4, -1], 
                                       [0, -1,  0]]),
                'Highpass':np.array([[-1, -1,  -1], 
                                       [-1,  8,  -1], 
                                       [-1, -1,  -1]]),
                'PrewittHx':np.array([[-1,  0, 1], 
                                       [-1,  0, 1], 
                                       [-1,  0, 1]]),
                'PrewittHy':np.array([[-1, -1, -1], 
                                       [0,   0,  0], 
                                       [1,   1,  1]]),
                'SobelHx':np.array([[-1, 0, 1], 
                                      [-2, 0, 2], 
                                      [-1, 0, 1]]),
                'SobelHy':np.array([[-1, -2, -1], 
                                      [0,   0,  0], 
                                      [1,   2,  1]]),}
    
    
    return(kernels[kernel])

def calculate_target_size(img_size: list, kernel_size: int) -> int:
    '''
    ## calculate_target_size()
    Calculates the target size of an image based on the kernel size.

    Parameters
    ----------
    img_size : list
        Size of the image (eg.: (200,300,3) for a RGB image)

    kernel_size : int
        Size of the kernel (eg.: (3) for a 3x3 kernel)
    '''
    num_pixels = 0
    x, y, _ = img_size
    # From 0 up to img size (if img size = 224, then up to 223)
    for i in range(x):
        # Add the kernel size (eg. 3) to the current i
        added = i + kernel_size
        # It must be lower than the image size
        if added <= x:
            # Increment if so
            num_pixels += 1 
    xpix = num_pixels
    num_pixels = 0
    for i in range(y):
        # Add the kernel size (eg. 3) to the current i
        added = i + kernel_size
        # It must be lower than the image size
        if added <= y:
            # Increment if so
            num_pixels += 1 
    ypix = num_pixels
    return(xpix, ypix)

def convert(image: np.ndarray) -> np.ndarray:
    '''
    ## convert()
    Convert float values to uint8, remapping the values.

    Parameters
    ----------
    image : np.ndarray
        Image to be converted
    '''
    target_type_max = 255
    target_type_min = 0
    target_type = np.uint8
    imin = image.min()
    imax = image.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    imagee = (a * image + b).astype(target_type)
    return imagee

def convolve(a=0):
    '''
    ## convolve()
    Colvolves an image called `img` with a global variable `kernel`.

    Parameters
    ----------
    a : any, optional
        Determines if the kernel will be given by getKernel() or by arbitraryKernel
    '''
    # Assuming a rectangular image
    IsLoaded() # check if the image is loaded
    global img
    global kernel
    global pb
    if a == 0:
        kernel = getKernel(combo_var.get())
    print(kernel)
    img = np.asarray(img)
    tgt_size = calculate_target_size(img_size=img.shape, kernel_size=kernel.shape[0])
    k = kernel.shape[0]
    
    # 3D array of zeros
    convolved_img = np.zeros(shape=(tgt_size[0], tgt_size[1], 3))

    # Iterate over the rows
    for i in range(tgt_size[0]):
        # Iterate over the columns
        for j in range(tgt_size[1]):
            for p in range(3): # over channels
                # img[i, j] = individual pixel value
                # Get the current matrix
                mat = img[i:i+k, j:j+k, p] # p = RGB
                
                summ = np.sum(np.multiply(mat, kernel))
                if summ < 0:
                    summ = 0
                convolved_img[i, j, p] = summ # p is R, G, B
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/tgt_size[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    img = Image.fromarray(convert(convolved_img))
    #img = Image.fromarray(ndimage.convolve(np.asarray(img), kernel))
    copy()

def arbitraryKernel():
    '''
    ## arbitraryKernel()
    Get as global variable `kernel`, an arbitrary kernel given by the user,
    and convolves with an image called `img`.
    '''
    IsLoaded() # check if the image is loaded
    new_window3 = Toplevel(window)
    new_window3.wm_geometry('250x75+250+330')
    new_window3.wm_title('Arbitrary Kernel')
    new_window3.focus_set()
    new_window3.grab_set()

    def getmatrix():
        global kernel
        kernel = np.zeros((3,3))
        for row in rows:
            for col in row:
                kernel[rows.index(row)][row.index(col)] = col.get()
        convolve(a=1)
        new_window3.destroy()

    rows = []
    for i in range(3):
        cols = []
        for j in range(3):
            e = Entry(new_window3,width=6)
            e.grid(row=i, column=j, sticky=NSEW)
            cols.append(e)
        rows.append(cols)

    apply = Button(new_window3, text = 'Convolve',
                 command = getmatrix,
                 height = 1, width = 6)
    apply.place(x=167, y=20)

def targetValue(val: int, target_arr: np.ndarray) -> Union[int, float]:
    '''
    ## findTargetValue()
    Find the taget value of a pixel to perform the histogram matching.

    Parameters
    ----------
    val : int
        Value to be searched
        
    target_arr : np.ndarray
        Numpy array to be used as target
    '''
    k = np.where(target_arr == val)[0] # find the first ocurrence where the target_arr[0] is equal to val

    if len(k) == 0: # if there is no occurrence
        k = targetValue(val+1, target_arr) # try val +1
        if len(k) == 0: # if there is no occurrence
            k = targetValue(val-1, target_arr) # try val -1
    val_aux = k[0]
    print('val_aux', val_aux)
    return val_aux

def matchHistogram():
    '''
    ## matchHistogram()
    Quantize both the image `img` and the target image `img2`, find the taget value of the 
    target pixel and perform the histogram matching within the image `img`.
    '''
    IsLoaded() # check if the image is loaded
    global img
    try:
        new_window2.destroy()
    except:
        pass
    ## open the image to be used as target (img2) ##
    def open_img():
        filename = filedialog.askopenfilename(initialdir=os.getcwd(
        ), title="Select file", filetypes=(("image files", ".png .jpg .bmp .jpeg .tif . tiff"), ("jpg images", ".jpg"), ("png images", ".png"), ("all files", "*.*")))
        if not filename:
            return

        global img2
        img2 = Image.open(filename) # open image pil
    open_img()
    inp_img = img2
    e_hist_input = histogramQuant(a=0) # get the quantized histogram for the original image
    e_hist_target = histogramQuant(a=1, b=1) # get the quantized histogram for the target image
    en_img = np.zeros_like(inp_img) # create the output image array
    tran_hist = np.zeros_like(e_hist_input)
    for i in range(len(e_hist_input)):
        tran_hist[i] = targetValue(val=e_hist_input[i], target_arr=e_hist_target)
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/e_hist_input*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    ## enhance image as well: ##
    for x_pixel in range(inp_img.shape[0]): # over columns
        for y_pixel in range(inp_img.shape[1]): # over rows
            pixel_val = int(inp_img[x_pixel, y_pixel])
            en_img[x_pixel, y_pixel] = tran_hist[pixel_val] # write the new pixel value
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/inp_img.shape[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    ## creating new histogram ##
    try:
        new_window2.destroy()
    except:
        pass
    calcHistogram(only_histo=0)
    img = en_img
    calcHistogram(a=1, b=320, title='Quantized Histogram', only_histo=0)
    copy()

def zoom():
    '''
    ## zoom()
    Applies independent zoom to x and y coordinates of an image called `img` 
    using the global variables `xfactor_val` and `yfactor_val` as zoom factors.
    '''
    IsLoaded() # check if the image is loaded
    global img

    width, height = img.size
    new_width = int(width/(1/float(xfactor_var.get())))-1 # uses the given xfactor to determine the new width
    new_height = int(height/(1/float(yfactor_var.get())))-1 # uses the given yfactor to determine the new height
    # Create a new empty image

    scaled_image = Image.new(img.mode, (new_width, new_height), 'white') # create a new image with the new size
    
    ## the factor is given by ##
    #xfactor = new_width/width
    #yfactor = new_height/height

    ## fill in every pixel in the scaled image ##
    for y in range(new_height): # over the rows
        for x in range(new_width): # over the columns
            x_nearest = int(np.round(x/xfactor_var.get())) # get the nearest pixel value in the rounded ratio for x
            y_nearest = int(np.round(y/yfactor_var.get())) # get the nearest pixel value in the rounded ratio for y

            pixel = img.getpixel((x_nearest, y_nearest))
            scaled_image.putpixel((x, y),  pixel) # write the new pixel to the new image
        window.update_idletasks() # update window to update progressbar
        pb['value'] = y/new_height*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0

    # Save it
    img = scaled_image
    copy()
    
rot_var = 0 # variable to track the rotation of the image

def rotateClock():
    '''
    ## rotateClock()
    Rotates an image called `img` clockwise by 90 degrees (-90 degrees).
    '''
    IsLoaded() # check if the image is loaded
    global img
    global rot_var # global variable used to determine the orientation of the image
    img_aux = np.asarray(img) # read as npArray
    _ = img_aux.shape
    img_aux_t = np.zeros((_[1],_[0],3)) # creates an array of zeros equal to the size of the rotated image
    for i in range(_[0]): # over the colums
        for j in range(_[1]): # over the rows
            img_aux_t[j][i] = img_aux[-i][j] # horario full
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/_[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    img = Image.fromarray(convert(img_aux_t)) # same as img_aux_t.astype(np.uint8)
    rot_var = not(rot_var) # update the global variable rot_var
    if rot_var == 1:
        r = int(img_aux.shape[0]/3)
    else:
        r = 0
    copy(r)

def rotateAntiClock():
    '''
    ## rotateAntiClock()
    Rotates an image called `img` counterclockwise by 90 degrees (+90 degrees).
    '''
    IsLoaded() # check if the image is loaded
    global img
    global rot_var # global variable used to determine the orientation of the image
    img_aux = np.asarray(img) # read as npArray
    _ = img_aux.shape
    img_aux_t = np.zeros((_[1],_[0],3)) # creates an array of zeros equal to the size of the rotated image
    for i in range(_[0]): # over the colums
        for j in range(_[1]): # over the rows
            img_aux_t[-j][i] = img_aux[i][j] # antihorario full
        window.update_idletasks() # update window to update progressbar
        pb['value'] = i/_[0]*100 # set progressbar value
    pb['value'] = 0 # when the loop finishes, set the value to 0
    img = Image.fromarray(convert(img_aux_t)) # same as img_aux_t.astype(np.uint8)
    rot_var = not(rot_var) # update the global variable rot_var
    if rot_var == 1:
        r = int(img_aux.shape[0]/3)
    else:
        r = 0
    copy(r)

## testing purposes ##
#def test():
#    print(combo_var.get())

#######################

def exit():
    '''
    ## exit()
    Close every window and so it's top widgets, and try to remove any auxiliary saved file.
    '''
    window.destroy() # destroy windows
    try:
        os.remove(f'{filename}_curr.jpg') # remove current image file (temp file)
    except:
        pass # ignore exceptions

## variable construction ##
option = IntVar()         # variable for flip LR or UD
quant_var = IntVar()      # variable for quantization
bright_var = IntVar()     # variable for brightness
cont_var = IntVar()       # variable for contrast
factor_state = IntVar()   # variable for factor/quantization
combo_var = StringVar()   # variable for combo menu (select kernel)
xfactor_var = DoubleVar() # variable for zoom xfactor (x axis)
yfactor_var = DoubleVar() # variable for zoom yfactor (y axis)

## further implementation - keep track of mouse position over the image ##
'''def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

new_window1.bind('<Motion>', motion)'''
