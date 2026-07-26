from image_manager import ImageManager
from slideshow import Slideshow
from drivesync import DriveSync
import pygame
from settings import *
from pathlib import Path

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

drivesync  = DriveSync("images")
drivesync.sync_to_drive()

img_manager = ImageManager(IMAGE_FOLDER)
slideshow = Slideshow(screen)

slideshow.load_next_surface(img_manager.current_image())
slideshow.display()
slideshow.load_next_surface(img_manager.next_image())

image_timer = pygame.time.get_ticks()
poll_timer = image_timer
running = True
while running:
    current_time = pygame.time.get_ticks()
    if current_time - image_timer > IMAGE_TIME: 
        slideshow.display()
        slideshow.load_next_surface(img_manager.next_image())
        image_timer = current_time
    if current_time - poll_timer > POLL_TIME:
        drivesync.sync_to_drive()
        img_manager.load_images()
        poll_timer = current_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

pygame.quit()