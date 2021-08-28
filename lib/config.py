import pygame
import os
import random
import numpy as np
import copy
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('dinogame-data-01ebf1e8f7b8.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('Dinogame Neuroevolution').sheet1

pygame.font.init()

WIN_WIDTH = 1920
WIN_HEIGHT = 1200
GROUND_POSITION = 670

START_POS = 150

START_LEVEL_SPEED = 35
LEVEL_SPEED_ACCEL = 0.02
MAX_LEVEL_SPEED = 175

level_speed = START_LEVEL_SPEED


DINOSAUR_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Dinosaur1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "DinosaurWalk1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "DinosaurWalk2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "DinosaurDuck1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "DinosaurDuck2.png"))),
]

CACTUS_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cactus1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cactus2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cactus3.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cactus4.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cactus5.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cactus6.png"))),
]

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Bird2.png"))),
]

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Ground.png")))
CLOUD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("Images", "Cloud.png")))

GEN_FONT = pygame.font.SysFont("monospace", 25)
SCORE_FONT = pygame.font.SysFont("monospace", 15)
INPUT_FONT = pygame.font.SysFont("monospace", 15)

POPULATION_SIZE = 125
