import pygame, sys

COLOR = (0, 0, 0)
SURFACE_COLOR = (0, 0, 0)

class Cart(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        pygame.draw.rect(self.image, color, pygame.Rect(50, 50, width, height))
        self.rect = self.image.get_rect()


def main():
    pygame.init()

    size = width, height = 600, 450
    speed = [2, 2]
    black = 0, 0, 0
    white = 255, 255, 255
    red = (255, 0, 0)
    screen = pygame.display.set_mode(size)
    all_sprites_list = pygame.sprite.Group()
    cart = Cart(red, 40, 40)
    cart.rect.x = 200
    cart.rect.y = 300
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
        print("finished drawing sprites")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
