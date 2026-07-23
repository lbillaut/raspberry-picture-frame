from image_manager import ImageManager
from slideshow import Slideshow
from drivesync import DriveSync
import pygame
from settings import *
from pathlib import Path


pygame.init()

running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))

drivesync  = DriveSync("shared_folder", "images")
drivesync.sync_to_drive()

img_manager = ImageManager(IMAGE_FOLDER)
slideshow = Slideshow(screen)

slideshow.display(img_manager.current_image())

start_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    if current_time - start_time > 5000: 
        slideshow.display(img_manager.next_image())
        start_time = current_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

pygame.quit()