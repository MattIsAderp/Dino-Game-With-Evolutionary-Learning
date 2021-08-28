from .config import *

class Dinosaur:
    JUMP_POWER = 14
    IMGS = DINOSAUR_IMGS
    ANIMATION_TIME = 5  # Amount of frames that one of the images will be shown

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.ducking = False
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        if self.y == 600:    # Can only jump while on ground
            self.vel = -self.JUMP_POWER
            self.tick_count = 0    # Reset tick_count

    def duck(self, duck):
        self.ducking = duck
        if duck == True and self.y < 600:
            self.vel = 15

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count**2    # The longer the dinosaur has been in the air, the slower he goes, eventually he falls down

        if d > 75:    # Terminal downwards velocity
            d = 75

        if d < 0:      # Tweaking the upwards velocity
            d -= 0

        if self.y + d >= 600:    # Don't fall through the ground
            self.y = 600
            d = 0

        self.y = self.y + d     # Apply the displacement to the dinosaur

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:    # For ANIMATION_TIME amount of frames, show this image
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 2:   # For ANIMATION_TIME amount of frames, show this image
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[1]
            self.img_count = 0    # As this is the last image of the animation, reset the img_count, and start over

        if self.y < 600:
            self.img = self.IMGS[0]

        if self.y >= 600 and self.ducking:
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[3]
            elif self.img_count < self.ANIMATION_TIME * 2:
                self.img = self.IMGS[4]
            elif self.img_count < self.ANIMATION_TIME * 3:
                self.img = self.IMGS[3]
                self.img_count = 0

        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
