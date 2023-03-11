# importing the modules #
from tkinter.ttk import Combobox
from functions import *

# defining window attributes #
window.title("Image Editor")
window.minsize(200, 330) # 200x300
window.geometry("+30+220")

# defining buttons and their functions #
button0 = Button(window, text="Open file", width=8, height=2, command = open_img_file)
button1 = Button(window, text ="Copy", width=8, height=2, command = copy_n)
button2 = Button(window, text ="Exit", width=8, height=2, command = exit)
button3 = Button(window, text ="Flip", width=8, height=1, command = flip_loop)
button4 = Button(window, text ="Grayscale", width=8, height=3, command = grayscale_loop)
button5 = Button(window, text ="Quantize", width=8, height=1, command = quantize)
button6 = Button(window, text ="Save file", width=8, height=3, command = save_img_file)

# NEW buttons (2-assigment) #
button7 = Button(window, text ="Brightness", width=8, height=1, command = brightAdjust)
button8 = Button(window, text ="Contrast", width=8, height=1, command = contAdjust)
button9 = Button(window, text ="Histogram", width=8, height=1, command = calcHistogram)
button10 = Button(window, text ="Invert", width=8, height=1, command = invert)
button11 = Button(window, text ="QuantHisto", width=8, height=1, command = histogramQuant)
button12 = Button(window, text ="Convolve", width=8, height=1, command = convolve)
button13 = Button(window, text ="Arbitrary", width=8, height=1, command = arbitraryKernel)
button14 = Button(window, text ="MatchHisto", width=8, height=1, command = matchHistogram)
button15 = Button(window, text ="Zoom(Sx,Sy)", width=8, height=1, command = zoom)
button16 = Button(window, text ="Rotate(90"+u'\N{DEGREE SIGN}'+")", width=8, height=1, command = rotateAntiClock)
button17 = Button(window, text ="Rotate(-90"+u'\N{DEGREE SIGN}'+")", width=8, height=1, command = rotateClock)
#button15 = Button(window, text ="test", width=8, height=1, command = test) # used for testing purposes

# buttons positions #
button0.grid(column=0, row=0)
button1.grid(column=1, row=0)
button2.grid(column=2, row=0)
button3.grid(column=0, row=1)
button4.grid(column=0, row=2)
button5.place(x=0, y=144)
button6.grid(column=2, row=3)

# NEW buttons positions (2-assigment) #
button7.place(x=95, y=79)
button8.place(x=95, y=113)
button9.place(x=95, y=144)
button10.grid(column=2, row=7)
button11.place(x=95, y=178)
button12.grid(column=0, row=4)
button13.grid(column=2, row=4)
button14.grid(column=2, row=6)
button15.grid(column=0, row=6)
button16.grid(column=0, row=7)
button17.grid(column=1, row=7)
#button15.grid(column=1, row=6) # used for testing purposes

# defining radiobuttons used for flip #
rad1 = Radiobutton(window, text='Horizontal', value=1, variable=option) # radiobutton for LR flip state
rad2 = Radiobutton(window, text='Vertical', value=2, variable=option)   # radiobutton for UD flip state

# radiobuttons positions for flip #
rad1.grid(column=1, row=1)
rad2.grid(column=2, row=1)

# defining radiobuttons for brightness and contrast #
rad3 = Radiobutton(window, text='V', value=0, variable=factor_state) # radiobutton for factor
rad4 = Radiobutton(window, text='F', value=1, variable=factor_state) # radiobutton for value

# radiobuttons positions for brightness and contrast #
rad3.place(x=240, y=83)
rad4.place(x=240, y=117)

# defining the default values of the variables #
quant_var.set(255) # variable for quantification
bright_var.set(0)  # variable for brightness
cont_var.set(0)    # variable for contrast

# defining spinboxes #
spin1 = Spinbox(window, from_= 0, to = 255, width=5, textvariable=quant_var)     # spin box for quantification
spin2 = Spinbox(window, from_= -255, to = 255, width=5, textvariable=bright_var) # spin box for brightness
spin3 = Spinbox(window, from_= 0, to = 255, width=5, textvariable=cont_var)      # spin box for contrast
spin4 = Spinbox(window, from_= 0, to = 6, width=3, textvariable=xfactor_var)     # spin box for zoom (x axis)
spin5 = Spinbox(window, from_= 0, to = 6, width=3, textvariable=yfactor_var)     # spin box for rotation (y axis)

# spinboxes positions #
spin1.place(x=16.5, y=178)
spin2.place(x=190, y=83)
spin3.place(x=190, y=117)
spin4.place(x=100.5, y=240)
spin5.place(x=140.5, y=240)

# combobox #
combo = Combobox(window, width=8, textvariable=combo_var)
combo['values'] = ('Gaussian', 'Laplacian', 'Highpass', 'PrewittHx', 
                   'PrewittHy', 'SobelHx', 'SobelHy')
#combo_var.set('Gaussian') # another option to set the default value for the combobox
combo.current(0)
combo.place(x=100.5, y=214)

window.mainloop() # mainloop
