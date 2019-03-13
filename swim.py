import pygame
import time
import math

#preliminaries for pygame 
from pygame.locals import *
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


#initialize pygame and load images here
pygame.init()
pygame.display.set_caption("SwimmWatch")
img1 = pygame.image.load("./figures/mainmenu.png")
img2 = pygame.image.load("./figures/start.png")
img2p1 = pygame.image.load("./figures/info.png")
img3 = pygame.image.load("./figures/timescreen.png")



myfont = pygame.font.SysFont('Comic Sans MS', 70)
myfont2 = pygame.font.SysFont('DJB Get Digital', 40)
textsurface = myfont.render(str(1), False, (255, 255, 255))


#sbutton = pygame.image.load("./figures/button.png")

#global variables
timer = 0
width = 800
height = 480
state = 1
nswimmers = 0


swimmers = [[False, 0, False, 0, False,  0], [False, 0, False,  0, False, 0], 
     [False, 0, False, 0, False,  0], [False, 0, False, 0, False,  0], 
     [False, 0, False, 0, False, 0]]


canvas = pygame.display.set_mode((width, height))
#canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
startingtime = time.time()
#some basic transformations for a better visualization
img1 = pygame.transform.scale(img1, (width, height))
img2 = pygame.transform.scale(img2, (width, height))
img2p1 = pygame.transform.scale(img2p1, (width, height))
img3 = pygame.transform.scale(img3, (width, height))

#handler for drawing canvas
def draw_handler(canvas):
	canvas.fill((0, 0, 0))
	if state == 1:
		canvas.blit(img1, (0,0))
	elif state ==2:
		canvas.blit(img2, (0,0))
		canvas.blit(textsurface,(256,25))
	elif state ==2.1: 
		canvas.blit(img2p1, (0,0))
	elif state == 3:
		canvas.blit(img3, (0,0))
		for i in range(0,5):
			swimmer = swimmers[i]
			time = swimmer[1]
			text = myfont2.render(str(format_time(time)), False, (0, 0, 0))
			canvas.blit(text,(241, 96+54*i))
			time = swimmer[3]
			text = myfont2.render(str(format_time(time)), False, (0, 0, 0))
			canvas.blit(text,(407, 96+54*i))
			time = swimmer[5]
			text = myfont2.render(str(format_time(time)), False, (0, 0, 0))
			canvas.blit(text,(573, 96+54*i))

	pygame.display.update()


def button(x, y, w, h, action=None):
	global state, nswimmers, textsurface, swimmers, startingtime
	mouse = pygame.mouse.get_pos()
	#click = pygame.mouse.get_pressed()
	#click = 1
	#print(click)
	#print(mouse)
	if x+w>mouse[0]>x and y+h > mouse[1] > y:
		if action=="exit":
			exit()
		elif action == "one-swimmer":
			nswimmers=1
			swimmers[0][0] = True
			swimmers[1][0] = False
			swimmers[2][0] = False
			swimmers[3][0] = False
			swimmers[4][0] = False
			state = 2
		elif action == "two-swimmers":
			nswimmers=2
			swimmers[0][0] = True
			swimmers[1][0] = True
			swimmers[2][0] = False
			swimmers[3][0] = False
			swimmers[4][0] = False
			state = 2
		elif action == "three-swimmers":
			nswimmers=3
			swimmers[0][0] = True
			swimmers[1][0] = True
			swimmers[2][0] = True
			swimmers[3][0] = False
			swimmers[4][0] = False
			state = 2
		elif action == "four-swimmers":
			nswimmers=4
			swimmers[0][0] = True
			swimmers[1][0] = True
			swimmers[2][0] = True
			swimmers[3][0] = True
			swimmers[4][0] = False
			state = 2
		elif action == "five-swimmers":
			nswimmers=5
			swimmers[0][0] = True
			swimmers[1][0] = True
			swimmers[2][0] = True
			swimmers[3][0] = True
			swimmers[4][0] = True
			state = 2
		elif action == "previous1":
			state = 1
		elif action == "info":
			state = 2.1
		elif action == "previous2":
			state = 2
		elif action == "start":
			state = 3
			for swimmer in swimmers:
				swimmer[1] =0
				swimmer[3] =0
				swimmer[5] =0
			startingtime = time.time()
		elif action == "previous3":
			state = 2
			resetswimmers()
		elif action == "stop":
			for swimmer in swimmers:
				swimmer[0] = False
		textsurface = myfont.render(str(nswimmers), False, (255, 255, 255))

def resetswimmers():
	global swimmers
	for i in range(0, 5):
		swimmers[i][0] = False
		swimmers[i][2] = False
		swimmers[i][4] = False
	for i in range(0, nswimmers):
		swimmers[i][0] = True

def format_time(time):
	msecs = (int(time*1000)//1)%1000
	if msecs<100:
		strmsecs = ".0"+str(msecs)
	else:
		strmsecs = "."+str(msecs)
	minutes = int(time)//60
	if minutes<10:
		strminutes = "0"+str(minutes)
	else:
		strminutes = str(minutes)
	time = time - 60*minutes
	secs = int(time)
	if secs<10:
		strsecs = ":0" + str(secs)
	else:
		strsecs = ":" + str(secs)
	if msecs==0 and minutes==0 and secs==0:
		return "--:--.---"
	return strminutes + strsecs + strmsecs

def sensor_pushed(key):
	global swimmers
	if key in [114, 103, 112, 121, 117]:
		swimmers_dict = {114:0, 103:1, 112:2, 121:3, 117:4}
		# r is key 114, g is key 103....
		#print(swimmers_dict[key])
		number = swimmers_dict[key]
		swimmer = swimmers[number]
		#print(swimmer)
		if swimmer[0] and not swimmer[2]:
			swimmer[2] = True
		elif swimmer[0] and swimmer[2] and not swimmer[4]:
			if swimmer[3]-swimmer[1] > 5:
				swimmer[4] = True
		print(swimmer)

def update_swimmers_time(swimmers):
	for swimmer in swimmers:
		if swimmer[0] and not swimmer[2]:
			swimmer[1] = time.time()-startingtime
		elif swimmer[0] and swimmer[2] and not swimmer[4]:
			swimmer[3] = time.time()- startingtime
		elif swimmer[0] and swimmer[2] and swimmer[4]:
			swimmer[5] = swimmer[3]-swimmer[1]

#main loop 
def main():
	global state, timer, swimmers
	running = True
	clock = pygame.time.Clock()
	click = pygame.mouse.get_pressed()
	#print(click)

	while running: 
		draw_handler(canvas)
		clock.tick(100)
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.MOUSEBUTTONUP:
				#print("Whohooooooo")
				button(615, 400, width-615, height-400, action = "exit")
				if state == 1:
					button(139, 240, 60, 70, action = "one-swimmer")
					button(253, 240, 60, 70, action = "two-swimmers")
					button(370, 240, 60, 70, action = "three-swimmers")
					button(485, 240, 60, 70, action = "four-swimmers")
					button(600, 240, 60, 70, action = "five-swimmers")
				elif state == 2:
					button(0, 393, 200, height-393, action= "previous1")
					button(703, 10, 90, 80, action = "info")
					button(295, 170, 205, 170, action = "start")
				elif state == 2.1:
					button(0, 393, 200, height-393, action= "previous2")
				elif state ==  3:
					button(0, 393, 200, height-393, action= "previous3")
					button(347, 382, 97, 95, action= "stop")
			if state == 3 and event.type == pygame.KEYDOWN:
					sensor_pushed(event.key)
		update_swimmers_time(swimmers)

	pygame.quit()

if __name__ == '__main__': main()