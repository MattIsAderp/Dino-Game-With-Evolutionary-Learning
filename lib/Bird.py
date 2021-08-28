from .config import *

class Bird:
    IMGS = BIRD_IMGS
    ANIMATION_TIME = 5

    def __init__(self, x):
        self.img = self.IMGS[0]
        self.x = x
        self.y = 650 - self.img.get_height() - random.randint(0,100)
        self.img_count = 0

        self.passed = False     # Check if the Cactus is behind the dino

    def move(self, spd):
        self.x -= spd     # Move the cactus by level_speed

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[0]
            self.img_count = 0

        win.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        dino_mask = dino.get_mask()     # Get the mask of the dino and the cactus
        bird_mask = pygame.mask.from_surface(self.img)

        offset = (int(self.x) - dino.x, self.y - round(dino.y))   # Get the offset of the two masks

        collision_point = dino_mask.overlap(bird_mask, offset)    # Check if the masks overlap, at the calculated offset

        if collision_point:
            return True

        return False
