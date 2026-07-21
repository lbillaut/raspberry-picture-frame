from image_manager import ImageManager
from slideshow import Slideshow
import pygame
from settings import *
from pathlib import Path

pygame.init()

running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))

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














# image_path = Path("images") / "red_rockpng.png"
# image = pygame.image.load(image_path)
# image = pygame.transform.scale(image, (WIDTH, HEIGHT))

# screen.blit(image, (0,0))

# pygame.display.flip()

# running = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 running = False

# pygame.quit()