# TODO
# Refactor code, make everything cleaner
# Convert to meters and seconds instead of pixels and frames
# Add an actual pid controller to move the cart to a certain position!

# IDEAS
# Add in a triangle such that when you drag it, the square will move to that position
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
        (Fx, Fy) = (z*math.cos(angle), z*math.sin(angle))
        (ax, ay) = (Fx / self.mass, Fy / self.mass)

        # update velocities
        self.vx += ax
        self.vy += ay

        return rect.move(self.vx, self.vy)

    def apply_force(self, force):
        self.force = force


def bob_acceleration(theta, ax, L, g=10):
    return (g *math.sin(theta) + -ax * math.cos(theta)) / L


def main():
    pygame.init()
    size = width, height = 600, 450
    speed = [2, 2]
    black = 0, 0, 0
    white = 255, 255, 255
    red = (255, 0, 0)
    screen = pygame.display.set_mode(size)
    all_sprites_list = pygame.sprite.Group()

    # cart params
    mcart = 20
    cart = Cart(red, 40, 40, mcart)
    cart.rect.x = 200
    cart.rect.y = 410
    rect_desired = 300
    kp = 0.1
    kd = 2
    error_old = rect_desired - cart.rect.x
    all_sprites_list.add(cart)
    ball = pygame.image.load("ball.jpeg")
    ball = pygame.transform.scale(ball, (20, 20))
    ballrect = ball.get_rect()
    clock = pygame.time.Clock()
    exit = True

    # Pendulum stuff
    L = 100
    theta = 0
    bob_r = 10
    bx = 200
    by = 360
    vbob = 0
    vbob_old = 0
    abob_old = 0
    theta = math.acos((by - cart.rect.y) / L)
    print("theta: %d", theta)
    while exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
        error = rect_desired - cart.rect.x
        derror = error - error_old
        (angle, z) = (0, int(kp * error) + int(kd * derror))
        #cart.force = (0, 0)
        cart.apply_force((angle, z))
        error_old = error
        all_sprites_list.update()
        screen.fill(SURFACE_COLOR)
        all_sprites_list.draw(screen)

        # calculate the new position of the bob
        (Fx, Fy) = (z * math.cos(angle), z * math.sin(angle))
        ax = Fx / mcart
        print("ax: %f", ax)
        abob = bob_acceleration(theta, ax, L)
        print("abob: %f", abob)
        vbob = abob - abob_old
        abob_old = abob
        #theta = vbob - vbob_old
        theta += 0.1
        vbob_old = vbob
        print("theta: %f", theta)
        bx = cart.rect.x + L * math.sin(theta)
        by = cart.rect.y - L * math.cos(theta)
        pygame.draw.circle(screen, red, (bx, by), bob_r)

        # draw the pendulum bob
        pygame.display.flip()
        clock.tick(10000)
    pygame.quit()


if __name__ == "__main__":
    main()
