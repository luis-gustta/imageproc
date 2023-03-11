### functions ###

## importing libraries ##
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
import os

from threading import Thread

from datetime import datetime

## OpenCV-Python ##
import cv2 as cv2

window = Tk()  # creating a top-level window called window

## creating the variables for the other windows ##
new_window2 = Toplevel(window)
new_window2.destroy()

#
output = cv2.VideoWriter()  # defining the initial state of the output variable
# rec = False

today = datetime.now()  # getting the initial value for today date and time
date_time = today.strftime("%Y%m%d_%H%M%S")  # format the date and time to be the timestamp (Ymd_HMS)
#
break_state = 0  # defining the initial state of the break_state variable


## beginning of the functions ##


class CoordinateColor:
    """
    Class that retains information about the coordinate of the cursor,
    and the RGB values at that coordinate.
    """
    def __init__(self, x, y):
        self.get_x = x  # pixel x-coordinate
        self.get_y = y  # pixel y-coordinate
        self.red = 0  # pixel R value
        self.green = 0  # pixel G value
        self.blue = 0  # pixel B value

    def get_color(self, image):  # method to get the color from the coordinates
        x, y = self.get_x, self.get_y
        try:
            self.red = image[y, x, 0]  # get R value from given image object (assuming RGB not BGR)
            self.green = image[y, x, 1]  # get G value from given image object
            self.blue = image[y, x, 2]  # get B value from given image object
        except IndexError:  # if image is grayscale (1D-color, R=G=B=L) -> IndexError (3D-color)
            try:
                luminance = image[y, x]  # try to get the luminance value
            except IndexError:
                luminance = 0  # if IndexError, then, luminance = 0
            self.red = luminance
            self.green = luminance
            self.blue = luminance

    def display(self):  # method to display the color in tkinter window
        coord_label.configure(text=f'(x={self.get_x}, y={self.get_y})')
        red_label.configure(text=f'R:{self.red}')
        green_label.configure(text=f'G:{self.green}')
        blue_label.configure(text=f'B:{self.blue}')


class ImageOperations:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """
    def __init__(self, dic):  # unpack the dictionary values into class attribute
        self.gray = dic['gray_val']  # grayscale variable
        self.save = 0  # saving state variable
        self.sobel = dic['sobel_val']  # sobel variable
        self.canny = dic['canny_val']  # canny variable
        self.gauss = False  # gaussian blur variable
        self.bright = False  # bright variable
        self.contrast = False  # contrast variable
        self.flipH = dic['flip_valH']  # horizontal flip variable
        self.flipV = dic['flip_valV']  # vertical flip variable
        self.invert = dic['invert_val']  # image negative variable
        self.resize = dic['resize_val']  # resize variable
        self.rotate = dic['rotate_val']  # rotate variable
        self.rec = False  # recording state variable
        self.is_loaded = 0  # loaded state variable

    def __str__(self):  # return a report of all the operations applied to the video
        description = f'Operations:\n' \
                      f'Loaded    : {bool(self.is_loaded)}\n' \
                      f'Grayscale = {bool(self.gray)}\n' \
                      f'Negative  = {bool(self.invert)}\n' \
                      f'Canny     = {bool(self.canny)}\n' \
                      f'Sobel     = {bool(self.sobel)}\n' \
                      f'GaussBlur = {self.gauss}\n' \
                      f'Bright    = {self.bright}\n'\
                      f'Contrast  = {self.contrast}\n' \
                      f'Hor. Flip = {bool(self.flipH)}\n' \
                      f'Ver. Flip = {bool(self.flipV)}\n' \
                      f'Rotate 90 = {bool(self.rotate)}\n' \
                      f'Resize    = {bool(self.resize)}\n' \
                      f'Recording : {bool(self.save)}\n'
        return description


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """
    def __init__(self, src=0):  # define the default video source (0=onboard_cam)
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.isOpen = False

    def start(self):  # method to start the video getter
        Thread(target=self.get, args=()).start()
        self.isOpen = True
        return self

    def get(self):  # method to get the video frame
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):  # method to stop video getter
        self.stopped = True
        self.isOpen = False


## initial attribute dictionary ##
init_dic = {'gray_val': 0, 'sobel_val': 0, 'canny_val': 0, 'flip_valH': 0,
            'flip_valV': 0, 'invert_val': 0, 'resize_val': 0, 'rotate_val': 0}

operations = ImageOperations(init_dic)  # creating the object to store the operations

pixel_hover = CoordinateColor(0, 0)  # creating the object to get and display the pixel colors

coord_label = Label(window, text=f'(x=0, y=0)')  # creating the Label object to display the pixel coordinate
coord_label.place(x=0, y=240)  # places the coord_label

## creating the Label objects to each channel (R, G, B) ##
red_label = Label(window, text='R:0', fg='red')
red_label.place(x=160, y=240)  # 110

green_label = Label(window, text='G:0', fg='green')
green_label.place(x=200, y=240)  # 150

blue_label = Label(window, text='B:0', fg='blue')
blue_label.place(x=240, y=240)  # 190


def start_camera(source=0):
    global new_window2, output  # defining the global variables

    button0.configure(state=DISABLED)  # deactivate the start camera button while camera is active

    # noinspection SpellCheckingInspection
    codec = cv2.VideoWriter_fourcc(*'XVID')  # defines the video codec to be used when saving

    new_window1 = Toplevel(window)  # create a new window on top of the main window, to display the original video
    new_window1.title('Original Video')  # title of new window 1
    new_window1.geometry("+330+220")  # position of new window 1
    new_window1.geometry("480x360")  # dimensions of the new window 1
    # new_window1.configure(bg='white')

    new_window2 = Toplevel(window)  # create a new window on top of the main window, to display the edited video
    new_window2.title('Edited Video')  # title of new window 2
    new_window2.geometry("+815+220")  # position of new window 2
    new_window2.geometry("480x360")  # dimensions of the new window 2
    # new_window2.configure(bg='white')

    def get_coord(event):  # function to get the coordinates of the cursor
        x_coord, y_coord = event.x, event.y  # get the coordinates from the given event
        pixel_hover.get_x = x_coord  # update the state of the 'get_x' attribute of pixel_hover
        pixel_hover.get_y = y_coord  # update the state of the 'get_y' attribute of pixel_hover

    new_window2.bind('<Motion>', get_coord)  # binding the function to the 'motion' event (when hovering new_window2)

    # bind close keys #
    new_window1.bind('<Destroy>', release_all)  # binding the closing window 1 event to the release_all function
    new_window2.bind('<Destroy>', release_all)  # binding the closing window 2 event to the release_all function

    # label = Label(new_window1, text="Image").pack()
    # label2 = Label(new_window2, text="Image2").pack()

    f1 = Label(new_window1)  # creating Label object for each window
    f2 = Label(new_window2)  #

    f1.pack()  # position the Label object, adjoins to the top side of the frame by default
    f2.pack()  #

    l1 = Label(f1)  # creating another Label object, within the created Label
    l2 = Label(f2)  #

    l1.pack()  # position the Label(Label) object, adjoins to the top side of the frame by default
    l2.pack()  #
    # source = 2
    video_getter = VideoGet(source).start()  # start the video_getter
    operations.is_loaded = 1  # update the state of the 'is_loaded' attribute (once the video capture is started)
    # main loop #
    while True:  # video capture main loop
        img_in = video_getter.frame  # get the frame from video_getter object
        img_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB)  # convert BGR -> RGB
        img_out = img_in.copy()  # create a copy of the original image
        if operations.gray:
            img_out = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)  # convert to grayscale
            img_out = cv2.cvtColor(img_out, cv2.COLOR_GRAY2RGB)  # convert grayscale size (1D) to RGB size (3D)
        if operations.sobel:
            img_aux = cv2.GaussianBlur(img_out, (5, 5), 0.9)  # gaussian blur as pre-processing
            img_out = cv2.Sobel(img_aux, cv2.CV_8UC1, 1, 1, ksize=5)  # apply sobel over x and y (1, 1)
            img_out = cv2.GaussianBlur(img_out, (3, 3), 0)  # gaussian blur to remove flickering and smooth the edges
        if operations.canny:
            img_aux = cv2.GaussianBlur(img_out, (3, 3), 0)  # gaussian blur as pre-processing
            img_out = cv2.Canny(image=img_aux, threshold1=50, threshold2=80)  # apply canny
            img_out = cv2.GaussianBlur(img_out, (5, 5), 0)  # gaussian blur to remove flickering and smooth the edges
        if operations.flipH:
            img_out = cv2.flip(img_out, 1)  # flip the image over y-axis
        if operations.flipV == 1:
            img_out = cv2.flip(img_out, 0)  # flip the image over x-axis
        if gauss_var.get() != 0:
            x = gauss_var.get()  # get the value of the trackbar
            img_out = cv2.GaussianBlur(img_out, (x, x), 0)  # use the value as the size of a gaussian kernel
        if bright_var.get() != 0:  # if the brightness trackbar is moved
            if bright_var.get() > 0:  # if the value is > 0
                shadow = bright_var.get()  # the shadow variable is updated
                highlight = 255
            else:  # if the value is not > 0 (-> value < 0)
                shadow = 0
                highlight = 255 + bright_var.get()  # the highlight variable is updated
            alpha_b = (highlight - shadow) / 255  # calculate the alpha
            gamma_b = shadow
            # once img_out is np.array, there is no method called .convertTo(), so cv2.addWeighted() instead
            img_out = cv2.addWeighted(img_out, alpha_b, img_out, 0, gamma_b)
        if cont_var.get() != 0:
            # get the contrast value from trackbar, and remaps the value
            f = float(131 * (cont_var.get() + 127)) / (127 * (131 - cont_var.get()))
            alpha_c = f  # the value is the new alpha
            gamma_c = 127 * (1 - f)  # the gamma is calculated from the alpha
            # once img_out is np.array, there is no method called .convertTo(), so cv2.addWeighted() instead
            img_out = cv2.addWeighted(img_out, alpha_c, img_out, 0, gamma_c)
        if operations.invert:
            img_out = 255 - img_out  # invert the colors of the image (negative)
        if operations.resize:
            _ = img_out.shape  # get the shape of the image
            # resize the image to half the original size, using area interpolation.
            # According to the documentation, area interpolation may be a preferred method
            # for image decimation, as it gives moire-free results, and is also faster than cubic
            img_out = cv2.resize(img_out, (int(_[1]/2), int(_[0]/2)), fx=0, fy=0, interpolation=cv2.INTER_AREA)
        if operations.rotate:
            # apply rotation by +90 degrees
            img_out = cv2.rotate(img_out, cv2.ROTATE_90_COUNTERCLOCKWISE)
            _ = img_out.shape  # get the shape of the image
            # update the window 2 geometry to keep the layout
            if operations.resize:
                new_window2.geometry("+815+220")  # 220
            else:
                new_window2.geometry("+815+170")

        if operations.rec is False and operations.save == 1:
            _ = img_out.shape  # get the shape of the image
            # create the VideoWriter object
            output = cv2.VideoWriter(f'{date_time}.avi', codec, 30, (_[1], _[0]))  # edited_video.avi
            operations.rec = True  # update the state of the rec attribute

        if operations.save == 1 and operations.rec is True:
            img_out_bgr = cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR)  # convert from RGB (for tkinter) back to BGR
            output.write(img_out_bgr)  # write the frame to the VideoWriter object

        # resize the img_in to display in tkinter window
        img_in = cv2.resize(img_in, (480, 360), fx=0, fy=0, interpolation=cv2.INTER_AREA)  # using INTER_AREA
        img_in = ImageTk.PhotoImage(Image.fromarray(img_in))  # convert the image to Tkinter PhotoImage
        # resize the img_out to display in tkinter window
        img_disp = cv2.resize(img_out, (480, 360), fx=0, fy=0, interpolation=cv2.INTER_AREA)  # using INTER_AREA

        if operations.resize == 1 and operations.rotate == 1:  # if the image is resized and rotated
            # resize the img_out to half the size of the rotated window 2 (360/2, 480/2)
            img_disp = cv2.resize(img_out, (180, 240), fx=0, fy=0, interpolation=cv2.INTER_AREA)  # using INTER_AREA
            new_window2.geometry(f"{180}x{240}")  # update the window 2 geometry
        elif operations.rotate:  # if the image is just rotated
            # resize the img_out the size of the rotated window 2 (360, 480)
            img_disp = cv2.resize(img_out, (360, 480), fx=0, fy=0, interpolation=cv2.INTER_AREA)  # using INTER_AREA
            new_window2.geometry(f"{360}x{480}")  # update the window 2 geometry
        elif operations.resize:  # if the image is just resized
            # resize the img_out to half the size of the window 2 (480/2, 360/2)
            img_disp = cv2.resize(img_out, (240, 180), fx=0, fy=0, interpolation=cv2.INTER_AREA)  # using INTER_AREA
            new_window2.geometry(f"{240}x{180}")  # update the window 2 geometry
        ##
        pixel_hover.get_color(img_disp)  # call the get_color method over the displayed edited image
        pixel_hover.display()  # call the display method to update the displayed coordinates and RGB values
        ##
        img_disp = ImageTk.PhotoImage(Image.fromarray(img_disp))  # convert the image to Tkinter PhotoImage

        l1['image'] = img_in  # update the Label(Label()) image attribute with the current frame
        l2['image'] = img_disp  #
        new_window1.update()  # update the window object
        new_window2.update()  #


def save_vid() -> None:
    """

    :return: None
    """
    global output, today, date_time  # global variables, once the output, today and date_time variables will be updated

    today = datetime.now()  # get the current date and time
    date_time = today.strftime("%Y%m%d_%H%M%S")  # format the date and time to be the timestamp (Ymd_HMS)

    is_loaded()  # tests if the video capture is started
    if operations.save == 1:  # if the video is being recorded and the button is pressed
        output.release()  # release the video capture
        operations.save = 0  # update the state of the 'save' attribute to 0
        operations.rec = False  # update the state of the 'rec' attribute to False
        button6.configure(text='Start Rec.', fg='black')  # change the color of the save button back to black
        button5.configure(state=NORMAL)  # when done recording, reactivate the resize button
        button12.configure(state=NORMAL)  # when done recording, reactivate the rotate button
        return
    # rec = not rec
    operations.save = 1  # update the state of the save attribute to 1 (True)
    if operations.rotate == 1:  # if the image is rotated, then,
        rotate()  # apply the 'rotation()' to undo the operation
    if operations.resize == 1:  # if the image is resized, then,
        resize()  # apply the 'resize()' to undo the operation
    button6.configure(text='Stop Rec.', fg='red')  # while recording, change the color of the save button to red
    button5.configure(state=DISABLED)  # while recording, deactivate the resize button
    button12.configure(state=DISABLED)  # while recording, deactivate the rotate button


# noinspection PyUnusedLocal

def release_all(*args: Event) -> None:
    """
    ## release_all(*args):
    Destroy every running python program. Grant that the camera will be released.

    :return: None
    """
    global break_state  # global variable, once the break_state variable will be updated

    if os.name == 'nt':  # if in windows
        # noinspection SpellCheckingInspection
        os.system('taskkill /im python.exe')  # destroy the running python (windows) TODO: test if working on windows
    else:
        os.system('pkill python')  # destroy the running python (linux or macOS)
    window.destroy()  # destroy the main window and all Toplevel windows
    break_state = 1  # update global variable break_state


def is_loaded() -> None:
    """
    ## is_loaded()
    Tests if the video capture is started or not. Ask the user to start the capture if necessary.

    :return: None
    """
    if operations.is_loaded != 1:  # if video capture not started
        a = messagebox.askyesno("Error", "Capture not started!",  # ask user to start the captureF
                                detail="Want to start the capture now?", icon='warning')
        if a:  # if yes
            start_camera()  # start the camera main loop
            return
        else:  # else, do nothing
            return


def copy() -> None:
    """
    ## copy()
    Change the current input video stream to the edited video window

    :return: None
    """
    global operations  # global variable, once the operations object will be updated

    is_loaded()  # tests if the video capture is started
    aux_var = operations.save  # auxiliary variable to save the state of the save attribute
    operations = ImageOperations(init_dic)  # updates every attribute to its original value
    operations.save = aux_var  # change the save attribute to the saved one
    gauss_var.set(0)  # set the non-boolean variables to 0 (the method 'set' from tkinter updates the attribute)
    bright_var.set(0)  #
    cont_var.set(0)  #
    operations.is_loaded = 1  # if the input is copied (pass the 'is_loaded' test), then the capture is started
    rad1.configure(value=1)  # return to the original values (if rotated)
    rad2.configure(value=2)  #
    new_window2.geometry("+815+220")  # update the window 2 (edited video) position to the original values
    new_window2.geometry("480x360")  # update the window 2 (edited video) geometry to the original values


def sobel() -> None:
    """
    ## sobel()
    Change the `sobel` state of the operations object.

    :return: None
    """
    is_loaded()  # tests if the video capture is started
    operations.sobel = not operations.sobel  # if False then True, if True then False


def canny() -> None:
    """
    ## canny()
    Change the `canny` state of the operations object.

    :return: None
    """
    is_loaded()  # tests if the video capture is started
    operations.canny = not operations.canny


def gaussian() -> None:
    """
    ## gaussian()
    Change the `gaussian` state of the operations object.

    :return: None
    """
    is_loaded()  # tests if the video capture is started
    if gauss_var.get() != 0:
        operations.gauss = 1  # if False then True, if True then False


def invert() -> None:
    """
    ## invert()
    Change the `invert` state of the operations object.

    :return: None
    """
    is_loaded()  # tests if the video capture is started
    operations.invert = not operations.invert  # if False then True, if True then False


def flip() -> None:
    """
    ## flip()
    Change the `flipH` or `flipV` state of the operations object.

    :return: None
    """
    is_loaded()  # tests if the video capture is started
    if flip_option.get() == 1:  # if option from radiobutton == 1, then flipH
        operations.flipH = not operations.flipH  # if False then True, if True then False

    elif flip_option.get() == 2:  # if option from radiobutton == 3, then flipV
        operations.flipV = not operations.flipV  # if False then True, if True then False


def grayscale() -> None:
    """
    ## grayscale()
    Change the `gray` state of the operations object.

    :return: None
    """
    is_loaded()  # tests if the video capture is started
    operations.gray = not operations.gray  # if False then True, if True then False


def resize() -> None:
    """
    ## resize()
    Change the `resize` state of the operations object.

    :return: None
    """
    global new_window2  # global variable, once the window position is updated

    is_loaded()  # tests if the video capture is started
    if operations.resize == 1:  # if already resized -> go back to original
        operations.resize = 0  # update the state of the resize attribute to the original value (if resized)
        new_window2.geometry("480x360")  # update the window 2 (edited video) geometry to the original values
        return
    operations.resize = 1  # update the state of the resize attribute


def rotate() -> None:
    """
    ## rotate()
    Change the `rotate` state of the operations object.

    :return: None
    """
    global new_window2  # global variable, once the window position is updated

    is_loaded()  # tests if the video capture is started
    if operations.rotate == 1:  # if already rotated -> go back to original
        operations.rotate = 0  # update the state of the rotate attribute to the original value (if rotated)
        new_window2.geometry("+815+220")  # update the window 2 (edited video) position to the original values
        new_window2.geometry("480x360")  # update the window 2 (edited video) geometry to the original values
        rad1.configure(value=1)  # return to the original values
        rad2.configure(value=2)  #
        return
    operations.rotate = 1  # update the state of the rotate attribute
    rad1.configure(value=2)  # once the image is rotated, the horizontal flip is now the vertical
    rad2.configure(value=1)  # and, the vertical flip is now the horizontal


#### new functions ####

def destroy_all() -> None:
    """
    ## destroy_all()
    Close all TopLevel-windows created on top of the window widget.

    :return: None
    """
    for widget in window.winfo_children():  # over the children of window
        if isinstance(widget, Toplevel):  # if is Toplevel window, then, destroy
            widget.destroy()


#######################


def exit_app() -> None:
    """
    ## exit()
    Close every window and so it's top widgets, and try to remove any auxiliary saved file.

    :return: None
    """
    operations.gauss = gauss_var.get()  # get the gaussian blur value to display on exit
    operations.bright = bright_var.get()  # get the bright value to display on exit
    operations.contrast = cont_var.get()  # get the contrast value to display on exit
    print(operations)  # print the operations applied to the video (report)
    window.destroy()  # destroy windows
    output.release()  # release the capture


## variable construction ##


flip_option = IntVar()  # variable for flip LR or UD
gauss_var = IntVar()  # variable for gaussian blur
bright_var = IntVar()  # variable for brightness
cont_var = IntVar()  # variable for contrast

# defining the buttons (that need to be updated during the running) #
button0 = Button(window, text="Open cam", width=8, height=2, command=start_camera)
button5 = Button(window, text="Resize (half)", width=8, height=1, command=resize)
button6 = Button(window, text="Start rec.", width=8, height=3, command=save_vid)
button12 = Button(window, text="Rotate (90" + u'\N{DEGREE SIGN})', width=8, height=1, command=rotate)

# defining radiobuttons used for flip (that need to be updated during the running) #
rad1 = Radiobutton(window, text='Horizontal', value=1, variable=flip_option)  # radiobutton for LR flip state
rad2 = Radiobutton(window, text='Vertical', value=2, variable=flip_option)  # radiobutton for UD flip state
