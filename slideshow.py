import pygame
from settings import *
from PIL import Image, ImageOps
import time

class Slideshow:
    def __init__(self, screen):
        self.screen = screen
        self.current_surface = None
        self.next_surface = None
    
    def display(self):
        self.screen.fill(BACKGROUND_RGB)    
        self.current_surface = self.next_surface
        center_x = (self.screen.get_width() - self.current_surface.get_width())/2
        center_y = (self.screen.get_height() - self.current_surface.get_height())/2
        self.screen.blit(self.current_surface, (center_x, center_y)) 
        pygame.display.flip()

    def scale_image(self, image):
        img_width = image.get_width()
        img_height = image.get_height()
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        aspect_ratio = img_width/img_height
        if aspect_ratio <= screen_width/screen_height:
            new_img_width = img_width*self.screen.get_height()/img_height
            new_img_height = screen_height
        else:
            new_img_width = screen_width
            new_img_height = img_height*self.screen.get_width()/img_width
        scaled_image = pygame.transform.scale(image, (int(new_img_width), int(new_img_height)))
        return scaled_image
    
    def load_next_surface(self, filename):
        start = time.perf_counter()
        """Loads an image, automatically fixes its EXIF orientation, 
        and returns a Pygame surface."""
        # 1. Open the image with Pillow
        with Image.open(filename) as img:
            # 2. Automatically check EXIF and correct orientation
            t = time.perf_counter()
            print(f"open: {t-start:.3f}s")
            img.draft("RGB", (self.screen.get_width(), self.screen.get_height()))
            img = ImageOps.exif_transpose(img)
            print(f"transpose: {time.perf_counter()-t:.3f}s")
            t = time.perf_counter()
            # 3. Scale to screen
            img.thumbnail((self.screen.get_width(), self.screen.get_height()))
            print(f"thumbnail: {time.perf_counter()-t:.3f}s")
            t = time.perf_counter()
            # 4. Convert the Pillow image data to a format Pygame understands
            image_bytes = img.tobytes()
            print(f"tobytes: {time.perf_counter()-t:.3f}s")
            t = time.perf_counter()
            image_size = img.size
            image_mode = img.mode # Usually 'RGB' or 'RGBA'
            
            self.next_surface = pygame.image.fromstring(image_bytes, image_size, image_mode)
            print(f"fromstring: {time.perf_counter()-t:.3f}s")

