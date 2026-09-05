# from image_manager import ImageManager
# from slideshow import Slideshow
# from drivesync import DriveSync
# import pygame
# from settings import *
# from pathlib import Path

# pygame.init()
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# drivesync  = DriveSync("images")
# drivesync.sync_to_drive()

# img_manager = ImageManager(IMAGE_FOLDER)
# slideshow = Slideshow(screen)

# slideshow.load_next_surface(img_manager.current_image())
# slideshow.display()
# slideshow.load_next_surface(img_manager.next_image())

# image_timer = pygame.time.get_ticks()
# poll_timer = image_timer
# running = True
# while running:
#     current_time = pygame.time.get_ticks()
#     if current_time - image_timer > IMAGE_TIME: 
#         slideshow.display()
#         slideshow.load_next_surface(img_manager.next_image())
#         image_timer = current_time
#     if current_time - poll_timer > POLL_TIME:
#         drivesync.sync_to_drive()
#         img_manager.load_images()
#         poll_timer = current_time
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             running = False

# pygame.quit()

from image_manager import ImageManager
from slideshow import Slideshow
from drivesync import DriveSync
import pygame
from settings import *
from pathlib import Path
import threading


pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

drivesync = DriveSync("images")
img_manager = ImageManager(IMAGE_FOLDER)
slideshow = Slideshow(screen)


# Event used to tell the background sync thread when to stop
stop_event = threading.Event()


def sync_loop():
    while not stop_event.is_set():
        try:
            drivesync.sync_to_drive()
            img_manager.load_images()
        except Exception as e:
            print(f"Sync failed: {e}")

        # Wait for POLL_TIME, but wake up immediately if the program exits
        stop_event.wait(POLL_TIME/1000)


# Start the Google Drive sync in the background
sync_thread = threading.Thread(target=sync_loop, daemon=True)
sync_thread.start()


# Start the slideshow immediately using whatever is already on the Pi
slideshow.load_next_surface(img_manager.current_image())
slideshow.display()
slideshow.load_next_surface(img_manager.next_image())


image_timer = pygame.time.get_ticks()
running = True

while running:
    current_time = pygame.time.get_ticks()

    if current_time - image_timer > IMAGE_TIME:
        slideshow.display()
        slideshow.load_next_surface(img_manager.next_image())
        image_timer = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False


# Tell the background thread to stop
stop_event.set()

pygame.quit()