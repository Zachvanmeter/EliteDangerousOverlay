from tkinter import *
from multiprocessing import Pipe
from win32gui import FindWindow, SetWindowLong
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE
import keyboard
from sys import exit
from itertools import cycle
from glob import glob

PATH_TO_RETICLES = 'Reticles\\'
MY_TITLE = 'ED Overlay'
BG_COLOR = '#000000'

class Hypnotherapy(Frame):
	def __init__(self, master, child, ReticlesCycle):
		Frame.__init__(self, master)
		self.master = master
		self.child = child
		self.ReticlesCycle = ReticlesCycle
		
		self.screenwidth = self.master.winfo_screenwidth()
		self.screenheight = self.master.winfo_screenheight()
		master.geometry('%dx%d' % (self.screenwidth, self.screenheight))
		master.overrideredirect(1)
		self.BuildReticle()
		self.Wait()
		
	def BuildReticle(self):
		self.c = Canvas(self,width=self.screenwidth,height=self.screenheight, highlightthickness=0,bg=BG_COLOR)
		self.img_object=next(self.ReticlesCycle)
		self.c.gif_create = self.c.create_image(self.screenwidth/2,self.screenheight/2,image=self.img_object)
		self.c.pack(fill=BOTH, expand=YES)
		self.ON = True
	
	def CycleReticle(self):
		self.img_object=next(self.ReticlesCycle)
		self.c.itemconfig(self.c.gif_create, image=self.img_object)
		
	def Wait(self):
		if self.child.poll() == True:
			Result = self.child.recv()
			if Result == 'Togle':
				if self.ON == True:
					self.c.itemconfig(self.c.gif_create, image='')
					self.ON = False
				else:
					self.c.itemconfig(self.c.gif_create, image=self.img_object)
					self.ON = True
			elif Result == 'Cycle':
				self.CycleReticle()
			elif Result == 'Exit':
				exit()
		self.master.after(500, self.Wait)

def WindowClickThrough(MyWindow):
	hwnd = FindWindow(None, MyWindow)
	windowStyles = WS_EX_LAYERED | WS_EX_TRANSPARENT
	SetWindowLong(hwnd, GWL_EXSTYLE, windowStyles)

def GenReticles():
	l =  [i for i in glob(PATH_TO_RETICLES+'*.png')]
	return cycle([(PhotoImage(file=image)) for image in l])
	
def OverlayExit():		parent.send('Exit');exit()
def OverlayTogle():		parent.send('Togle')
def OverlayCycle():		parent.send('Cycle')

def launch():
	root = Tk()
	
	root.wm_attributes("-topmost", 1)
	root.wm_attributes("-transparentcolor", BG_COLOR)
	root.configure(background=BG_COLOR)
	
	Opacity = 1.0 
	root.attributes('-alpha', Opacity)
	
	root.title(MY_TITLE)
	WindowClickThrough(MY_TITLE)
	
	ReticlesCycle = GenReticles()
	e = Hypnotherapy(root, child, ReticlesCycle)
	e.pack(fill=BOTH, expand=YES)
	root.mainloop()
	
	
if __name__ == '__main__':
	parent,child = Pipe()
	keyboard.add_hotkey('left+0', OverlayExit)
	keyboard.add_hotkey('left+down', OverlayTogle)
	keyboard.add_hotkey('right+down', OverlayCycle)
	launch()
