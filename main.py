import pygame
import os
import sys
import random

pygame.init()
size = width, height = 550, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()
fumigator = pygame.sprite.Group()
platforms = pygame.sprite.Group()
background = load_image("eiffel.png")
background = pygame.transform.scale(background, (550, 600))


class Islands(pygame.sprite.Sprite):
    def __init__(self, x, hgt, *group):
        super().__init__(platforms)
        self.image = load_image('baget.png')
        # self.image = pygame.transform.scale(self.image, (205, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = hgt

    def update(self, upp):
        self.rect.y += upp
        if self.rect.top > 600:
            self.kill()


class Fumigator(pygame.sprite.Sprite):
    def __init__(self, x, hgt, *group):
        super().__init__(fumigator)
        self.image = load_image('fumigator.jpg', -1)
        self.image = pygame.transform.scale(self.image, (105, 55))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = hgt

    def update(self, upp):
        self.rect.y += upp
        if self.rect.top > 600:
            self.kill()


class Komar(pygame.sprite.Sprite):
    image = load_image("komar.png")

    def __init__(self, *group):
        super().__init__(all_sprites)
        self.image = Komar.image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        self.rect.center = (350, 300)
        self.side = False

    def play(self, frst):
        up = 0
        dx = 0
        dy = 0
        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_LEFT]:
            dx = -10
            self.side = True
        elif userInput[pygame.K_RIGHT]:
            dx = 10
            self.side = False
        elif userInput[pygame.K_UP]:
            dy = -10
        elif userInput[pygame.K_DOWN]:
            dy = 10

        self.velocity += 1
        dy += self.velocity

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 550:
            dx = 550 - self.rect.right

        collision_plat = pygame.sprite.spritecollide(self, platforms, False)
        if collision_plat:
            if self.rect.bottom < collision_plat[0].rect.bottom:
                if self.velocity > 0:
                    self.rect.bottom = collision_plat[0].rect.top
                    dy = 0
                    self.velocity = -20
        if pygame.sprite.spritecollideany(self, fumigator):
            self.kill()
        if frst:
            if self.rect.bottom + dy > 600:
                dy = 0
                self.velocity = -20
            # else:
            #     dy = 0
            #     self.ve

        if self.rect.top <= 200:
            if self.velocity < 0:
                up = -dy

        self.rect.x += dx
        self.rect.y += dy + up

        if self.rect.top > 600:
            self.kill()

        return up


switch = True
komar = Komar()
all_sprites.add(komar)


class GameStates():
    def __init__(self):
        self.state = 'intro'
        self.start = True
        self.limit = 15
        self.switch = True
        self.h = 400
        self.island = Islands(222, 440)
        self.fumigator = Fumigator(222, 440)
        platforms.add(self.island)

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'

        pygame.display.flip()

    def main_game(self):
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.start = False
        up = komar.play(self.start)
        if len(all_sprites) == 1:
            screen.blit(background, (0, 0))
            all_sprites.draw(screen)
            platforms.draw(screen)
        else:
            end_screen()
        if len(platforms) < self.limit:
            for _ in range(2):
                num_x = random.randint(-100, 350)
                num_y = self.island.rect.y - random.randint(90, 110)
                num_x1 = random.randint(-70, 400)
                num_y1 = self.island.rect.y - random.randint(90, 110)
                if _ == 0:
                    if self.switch:
                        self.island = Islands(num_x, num_y)
                        self.fumigator = Fumigator(num_x1, num_y1)
                        self.switch = False
                    else:
                        self.island = Islands(num_x + random.randint(250, 350), num_y)
                        self.fumigator = Fumigator(num_x + random.randint(200, 400), num_y)
                        self.switch = True
                    platforms.add(self.island)
                else:
                    if self.switch:
                        self.island = Islands(num_x, num_y)
                        self.switch = False
                    else:
                        self.island = Islands(num_x + random.randint(250, 350), num_y)
                        self.switch = True
                    platforms.add(self.island)
        platforms.update(up)
        pygame.display.flip()

    def state_image(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()


game_state = GameStates()


def start_screen():
    global gr, x, y
    intro_text = ["Komar-parizhanin", "",
                  "welcome"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(pygame.transform.scale(fon, [200, 200]), (150, 150))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for i in intro_text:
        text_welcome = font.render(i, True, (255, 255, 255))
        intro_rect = text_welcome.get_rect()
        intro_rect.center = (500, 00)
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(text_welcome, intro_rect)


def end_screen():
    global gr, x, y
    screen.fill((0, 0, 0))
    intro_text = ["score: ", "",
                  "from zhamilya and dameli", "", "", "", "",
                  "thanks!"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(pygame.transform.scale(fon, [200, 200]), (150, 150))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for i in intro_text:
        text_welcome = font.render(i, True, (255, 255, 255))
        intro_rect = text_welcome.get_rect()
        intro_rect.center = (500, 00)
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 170
        text_coord += intro_rect.height
        screen.blit(text_welcome, intro_rect)

    pygame.display.update()


start_screen()
while True:
    game_state.state_image()
