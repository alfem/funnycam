#!/usr/bin/python

# Funnycam 1.0
# Mezcla una webcam con un decorado para hacer capturas graciosas
# Copyright Alfonso E.M. 2009
# Este programa se distribuye bajo los términos de la licencia GPL (General Public License) versión 2.0



import pygame
import Image
from pygame.locals import *
import sys
from PIL import ImageEnhance
from PIL import ImageOps

import opencv

#this is important for capturing/displaying images
from opencv import highgui 

XSCALE=640
YSCALE=480
BRIGHTNESS=3.0


camera = highgui.cvCreateCameraCapture(0)

def get_image():
    im = highgui.cvQueryFrame(camera)

# Add the line below if you need it (Ubuntu 8.04+)
    im = opencv.cvGetMat(im)


# Resize image if needed
    resized_im=opencv.cvCreateImage(opencv.cvSize(XSCALE,YSCALE),8,3)
    opencv.cvResize( im, resized_im, opencv.CV_INTER_CUBIC);

#convert Ipl image to PIL image
    pil_img = opencv.adaptors.Ipl2PIL(resized_im)

    enhancer=ImageEnhance.Brightness(pil_img)
    pil_img=enhancer.enhance(BRIGHTNESS)
    pil_img=ImageOps.mirror(pil_img)

    return pil_img

def load_image(name, colorkey=None):
    fullname = name
    try:
      image = pygame.image.load(fullname)
    except pygame.error, message:
      print 'Cannot load image:', name
      raise SystemExit, message
      image = image.convert()
    if colorkey is not None:
      if colorkey is -1:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
                                                                            

fps = 30.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("Guadalinex Foto Stand")
screen = pygame.display.get_surface()
costume1,costume1_rect1= load_image("andatuz1.png")

costume=0

while True:

    webcam = get_image()

    pg_img = pygame.image.frombuffer(webcam.tostring(), webcam.size, webcam.mode)
    screen.blit(pg_img, (0,0))

    if costume==1:
      screen.blit(costume1, (0,0))

    pygame.display.flip()

    events = pygame.event.get()
    for event in events:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or event.type ==QUIT:
                sys.exit()
        if keys[pygame.K_1]:
          costume=1          
        if keys[pygame.K_0]:
          costume=0          
        if keys[pygame.K_PLUS]:
          BRIGHTNESS+=0.1          
        if keys[pygame.K_MINUS]:
          BRIGHTNESS-=0.1          
        if keys[pygame.K_SPACE]:
          print "Capturing..."
          pygame.image.save(screen,"test.jpg")          

    pygame.time.delay(int(1000 * 1.0/fps))
