import os
import pygame

# TODU: dynamisk BASE_IMG_PATH
BASE_IMG_PATH = 'assets/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((255, 255, 255))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images