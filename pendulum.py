import pygame
import time
import numpy as np
import math

# Pendulum physics params
g = 9.8 # gravity constant
l = 0.3 # length of pendulum stick in meters
m = 0.1 # mass of the pendulum (kg)
r = 0.05 # radius of the pendulum
av_max = 2 # max angular velocity in radians/sec

# Conversion params
PIXELS_PER_METER = 100
FPS = 80
DELTA_T = 1/FPS

# Pendulum state-space matrices
A = np.array([
    [0, 1],
    [-g/l, 0],
])
B = np.array([[0], [1/(m*l*l)]])

# Pygame global variables
width = 600
height = 450
screen = pygame.display.set_mode((width, height))
SURFACE_COLOR = (0, 0, 0)
all_sprites_list = pygame.sprite.Group()


class Bob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = r*PIXELS_PER_METER
        diameter = 2*radius
        self.image = pygame.Surface([diameter, diameter])
        self.image.fill(SURFACE_COLOR)
        color = (255, 0, 0)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()


def main():
    T = 0
    theta = math.pi / 8
    state = np.array([[theta], [0]])  # Initial angle: theta, Initial angular velocity: 0

    # initialize pendulum bob
    bob = Bob()
    origin = (200, 200)
    bob.rect.x = origin[0]
    bob.rect.y = origin[1]
    all_sprites_list.add(bob)

    exit = True
    clock = pygame.time.Clock()
    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False

        # pendulum state calculation
        state = np.sum([state, DELTA_T * np.dot(A, state)], axis=0)
        state[0][0] = np.clip(state[0][0], -av_max, av_max)
        bob.rect.y = origin[1] + l*PIXELS_PER_METER*math.cos(state[0][0])
        bob.rect.x = origin[0] + l*PIXELS_PER_METER*math.sin(state[0][0])
        print(state)
        all_sprites_list.update()
        screen.fill(SURFACE_COLOR)
        all_sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()