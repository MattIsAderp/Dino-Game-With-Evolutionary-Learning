from .config import *

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Ground.png")))
GROUND_POSITION = 670

class Ground:
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self):
        self.y = GROUND_POSITION
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, spd):
        self.x1 -= spd
        self.x2 -= spd

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
