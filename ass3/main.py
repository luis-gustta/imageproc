# importing the modules #
from functions import *
# from tkinter import ttk

# defining window attributes #
window.title("Video Processing")  # set the title of the main window
window.minsize(200, 260)  # 200x240 # 200x300 # set the minimum size of the main window
window.geometry("+30+220")  # position of the main window
photo = PhotoImage(file=os.getcwd()+'/icon.png')  # load the icon image as Tkinter PhotoImage
window.iconphoto(False, photo)  # use the loaded PhotoImage as the icon
# window.bind('<Destroy>', release_all)

# defining buttons and their functions #
# button0 defined in functions.py
button1 = Button(window, text="Copy", width=8, height=2, command=copy)
button2 = Button(window, text="Exit", width=8, height=2, command=exit_app)
button3 = Button(window, text="Flip", width=8, height=1, command=flip)
button4 = Button(window, text="Grayscale", width=8, height=1, command=grayscale)

# NEW buttons (2-assigment) #
button9 = Button(window, text="Invert", width=8, height=1, command=invert)
button10 = Button(window, text="Canny", width=8, height=1, command=canny)
button11 = Button(window, text="Sobel", width=8, height=1, command=sobel)
# button15 = Button(window, text ="test", width=8, height=1, command = test) # used for testing purposes

# buttons positions #
button0.grid(column=0, row=0)
button1.grid(column=1, row=0)
button2.grid(column=2, row=0)
button3.grid(column=0, row=1)
button4.grid(column=0, row=2)
button5.place(x=0, y=175)
button6.place(x=190, y=175)  # grid(column=2, row=7)

# NEW buttons positions (2-assigment) #
button9.place(x=95, y=175)
button10.place(x=0, y=209)
button11.place(x=95, y=209)
button12.place(x=0, y=113)
# button15.grid(column=1, row=6) # used for testing purposes

# radiobuttons positions for flip #
rad1.grid(column=1, row=1)
rad2.grid(column=2, row=1)

# defining the default values of the variables #
bright_var.set(0)  # variable for brightness
cont_var.set(0)  # variable for contrast

# defining slider #
gauss_bar = Scale(window, from_=1, to=99, resolution=2, orient=HORIZONTAL,
                  length=183, variable=gauss_var, showvalue=False)
gauss_bar.set(0)

bright_bar = Scale(window, from_=-255, to=255, resolution=1, orient=HORIZONTAL,
                   length=108, variable=bright_var, showvalue=False)
bright_bar.set(0)

contrast_bar = Scale(window, from_=-127, to=127, resolution=2, orient=HORIZONTAL,
                     length=108, variable=cont_var, showvalue=False)
contrast_bar.set(0)

# slider position #
gauss_bar.place(x=95, y=149)
bright_bar.place(x=170, y=85)
contrast_bar.place(x=170, y=119)

# defining the labels #
bright_label = Label(window, text='Brightness')  # for brightness
bright_label.place(x=95, y=85)

contrast_label = Label(window, text='Contrast')  # for contrast
contrast_label.place(x=95, y=119)

gauss_label = Label(window, text='Gaussian Blur')  # for Gaussian Blur
gauss_label.place(x=0, y=149)

window.mainloop()  # mainloop
