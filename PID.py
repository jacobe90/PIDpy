# TODO
# Refactor code, make everything cleaner
# Convert to meters and seconds instead of pixels and frames
# Add an actual pid controller to move the cart to a certain position!

import pygame, sys, math

COLOR = (0, 0, 0)
SURFACE_COLOR = (0, 0, 0)

class Cart(pygame.sprite.Sprite):
    def __init__(self, color, width, height, mass):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        pygame.draw.rect(self.image, color, pygame.Rect(50, 50, width, height))
        self.rect = self.image.get_rect()
        self.force = (0, 2)
        self.vx, self.vy = 0, 0
        self.mass = mass
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def update(self):
        newpos = self.calcnewpos(self.rect, self.force)
        self.rect = newpos
        (angle, z) = self.force
        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or (br and bl):
                angle = -angle
            if tl and bl:
                # self.offcourt()
                angle = math.pi - angle
            if tr and br:
                angle = math.pi - angle
        self.force = (angle, z)


    def calcnewpos(self, rect, force):
        (angle,z) = force
        (Fx, Fy) = (z*math.cos(angle),z*math.sin(angle))
        (ax, ay) = (Fx / self.mass, Fy / self.mass)

        # update velocities
        self.vx += ax
        self.vy += ay

        return rect.move(self.vx, self.vy)

    def apply_force(self, force):
        self.force = force

def main():
    pygame.init()
    size = width, height = 600, 450
    speed = [2, 2]
    black = 0, 0, 0
    white = 255, 255, 255
    red = (255, 0, 0)
    screen = pygame.display.set_mode(size)
    all_sprites_list = pygame.sprite.Group()
    cart = Cart(red, 40, 40, 20)
    cart.rect.x = 200
    cart.rect.y = 410
    all_sprites_list.add(cart)
    ball = pygame.image.load("ball.jpeg")
    ball = pygame.transform.scale(ball, (20, 20))
    ballrect = ball.get_rect()
    clock = pygame.time.Clock()
    exit = True
    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False

        all_sprites_list.update()
        screen.fill(SURFACE_COLOR)
        all_sprites_list.draw(screen)
        # print("finished drawing sprites")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
