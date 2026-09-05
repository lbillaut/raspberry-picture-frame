# from pathlib import Path

# # imagemanager should deal with image paths, not actually load images into memory because that's wasteful. 
# # slideshow.py should do this. 
# class ImageManager:
#     def __init__(self, image_folder):
#         self.image_folder = Path(image_folder)
#         self.images = []
#         self.current_index = 0
#         self.load_images()

#     def load_images(self):
#         extensions = {".jpg", ".jpeg", ".png", ".bmp"}
#         self.images = [
#             file 
#             for file in self.image_folder.iterdir()
#             if file.suffix.lower() in extensions
#         ]

#         self.images.sort()

#         print(f"Loaded {len(self.images)} images.")
    
#     def current_image(self):
#         return self.images[self.current_index]
    
#     def next_image(self):
#         self.current_index += 1
#         self.current_index = (self.current_index) % len(self.images)
#         return self.current_image()

from pathlib import Path
import threading


# ImageManager deals with image paths, not image data.
# Slideshow.py actually loads images into memory.


class ImageManager:
    def __init__(self, image_folder):
        self.image_folder = Path(image_folder)
        self.images = []
        self.current_index = 0
        self.lock = threading.Lock()

        self.load_images()

    def load_images(self):
        extensions = {".jpg", ".jpeg", ".png", ".bmp"}

        new_images = [
            file
            for file in self.image_folder.iterdir()
            if file.suffix.lower() in extensions
        ]

        new_images.sort()

        with self.lock:
            self.images = new_images

            if len(self.images) == 0:
                self.current_index = 0
            else:
                self.current_index %= len(self.images)

        print(f"Loaded {len(self.images)} images.")

    def current_image(self):
        with self.lock:
            return self.images[self.current_index]

    def next_image(self):
        with self.lock:
            self.current_index += 1
            self.current_index %= len(self.images)

            return self.images[self.current_index]