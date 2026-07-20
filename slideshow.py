import pygame

class Slideshow:
    def __init__(self, screen):
        self.screen = screen
    
    def display(self, image_path):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0,0))
        pygame.display.flip()
        # time = pygame.time.get_ticks()
        # return time
