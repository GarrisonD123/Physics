#! /usr/bin/env python
from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
else:
    from tkinter import *
    import tkinter as Tk

wavelength=632.8*nm #wavelength of HeNe laser
size=10*mm # size of the grid
N=300 # number (NxN) of grid pixels
R=3*mm # laser beam radius
z1=8*cm # length of arm 1
z2=7*cm # length of arm 2
z3=3*cm # distance laser to beamsplitter
z4=5*cm # distance beamsplitter to screen
Rbs=0.5 # reflection beam splitter
tx=1*mrad; ty=0.0*mrad # tilt of mirror 1
f=50*cm # focal length of positive lens
root = Tk.Tk()

def update():
    z2 = scalez2.get()*cm
    tx = scaletx.get()*mrad
    ty = scalety.get() * mrad
    expirement(z2, tx,ty)


scalez2 = Tk.Scale(root, orient='horizontal', label='length movable arm[cm]', length=200, from_=1, to=100)
scalez2.pack()
scaletx = Tk.Scale(root, orient='horizontal', label='horizontal mirror tilt[mrad]', length=200, from_=0, to=5,resolution = .01)
scaletx.pack()
scalety = Tk.Scale(root, orient='horizontal', label='vertical mirror tilt[mrad]', length=200, from_=0, to=5,resolution = .01)
scalety.pack()
update_btn = Button(root, text="Click to update", command=update).pack()


def expirement(z2,tx,ty):

    #Generate a weak converging laser beam using a weak positive lens:
    F=Begin(size,wavelength,N)
    #F=GaussBeam(F, R)
    #F=GaussHermite(F,R,0,0,1) #new style
    #F=GaussHermite(F,R) #new style
    F=GaussHermite(0,0,1,R,F) #old style
    F=Lens(f,0,0,F)

    #Propagate to the beamsplitter:
    F=Forvard(z3,F)

    #Split the beam and propagate to mirror #2:
    F2=IntAttenuator(1-Rbs,F)
    F2=Forvard(z2,F2)

    #Introduce tilt and propagate back to the beamsplitter:
    F2=Tilt(tx,ty,F2)
    F2=Forvard(z2,F2)
    F2=IntAttenuator(Rbs,F2)

    #Split off the second beam and propagate to- and back from the mirror #1:
    F10=IntAttenuator(Rbs,F)
    F1=Forvard(z1*2,F10)
    F1=IntAttenuator(1-Rbs,F1)

    #Recombine the two beams and propagate to the screen:
    F=BeamMix(F1,F2)
    F=Forvard(z4,F)
    I=Intensity(1,F)

    plt.imshow(I, cmap='jet');
    plt.axis('off');
    plt.title('intensity pattern')
    plt.show()


root.mainloop()