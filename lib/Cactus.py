from .config import *

class Cactus:
    IMGS = CACTUS_IMGS

    def __init__(self, x):
        self.x = x
        self.img = self.IMGS[random.randint(0, len(self.IMGS) - 1)]    # Pick a random cactus from the list CACTUS_IMGS
        self.y = 695 - self.img.get_height()

        self.passed = False     # Check if the Cactus is behind the dino

    def move(self, spd):
        self.x -= spd     # Move the cactus by level_speed

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        dino_mask = dino.get_mask()     # Get the mask of the dino and the cactus
        cactus_mask = pygame.mask.from_surface(self.img)

        offset = (int(self.x) - dino.x, self.y - round(dino.y))   # Get the offset of the two masks

        collision_point = dino_mask.overlap(cactus_mask, offset)    # Check if the masks overlap, at the calculated offset

        if collision_point:
            return True

        return False
