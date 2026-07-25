from pathlib import Path

# imagemanager should deal with image paths, not actually load images into memory because that's wasteful. 
# slideshow.py should do this. 
class ImageManager:
    def __init__(self, image_folder):
        self.image_folder = Path(image_folder)
        self.images = []
        self.current_index = 0
        self.load_images()

    def load_images(self):
        extensions = {".jpg", ".jpeg", ".png", ".bmp"}
        self.images = [
            file 
            for file in self.image_folder.iterdir()
            if file.suffix.lower() in extensions
        ]

        self.images.sort()

        print(f"Loaded {len(self.images)} images.")
    
    def current_image(self):
        return self.images[self.current_index]
    
    def next_image(self):
        self.current_index += 1
        self.current_index = (self.current_index) % len(self.images)
        return self.current_image()
