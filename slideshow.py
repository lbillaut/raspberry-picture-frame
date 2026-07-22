import pygame
from settings import *

class Slideshow:
    def __init__(self, screen):
        self.screen = screen
    
    def display(self, image_path):
        self.screen.fill(BACKGROUND_RGB)    
        image = pygame.image.load(image_path)
        scaled_image = self.scale_image(image)
        center_x = (self.screen.get_width() - scaled_image.get_width())/2
        center_y = (self.screen.get_height() - scaled_image.get_height())/2
        self.screen.blit(scaled_image, (center_x, center_y)) 
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