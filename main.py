import pygame
import os
import sys
import random

pygame.init()
size = width, height = 550, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None): # функция загрузки картинок
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group() # спрайты
fumigator = pygame.sprite.Group()
platforms = pygame.sprite.Group()
background = load_image("eiffel.png")
background = pygame.transform.scale(background, (550, 600))


class Islands(pygame.sprite.Sprite): # класс для островов
    def __init__(self, x, hgt, *group):
        super().__init__(platforms)
        self.image = load_image('baget.png')
        self.image = pygame.transform.scale(self.image, (205, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = hgt
         # бесконечные острова

    def update(self, upp):
        self.rect.y += upp
        if self.rect.top > 600:
            self.kill()


class Fumigator(pygame.sprite.Sprite):# класс для фумигаторов
    def __init__(self, x, hgt, *group):
        super().__init__(fumigator)
        self.image = load_image('fumigator.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = hgt
         # бесконечные фумигаторы

    def update(self, upp):
        self.rect.y += upp
        if self.rect.top > 600:
            self.kill()


class Komar(pygame.sprite.Sprite): # класс для комара
    image = load_image("komar.png")

    def __init__(self, *group):
        super().__init__(all_sprites)
        self.image = Komar.image
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 0
        self.rect.center = (280, 300)
        self.side = False
        self.score = 0

    def play(self, frst):
        up = 0
        dx = 0
        dy = 0
        userInput = pygame.key.get_pressed()
        # движение комара

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
            # столкновение с островами

        collision_plat = pygame.sprite.spritecollide(self, platforms, False)
        if collision_plat:
            if self.rect.bottom < collision_plat[0].rect.bottom:
                if self.velocity > 0:
                    self.rect.bottom = collision_plat[0].rect.top
                    dy = 0
                    self.velocity = -20
                    self.score += 1
        if pygame.sprite.spritecollideany(self, fumigator):
            self.kill()

        if frst:
            if self.rect.bottom + dy > 600:
                dy = 0
                self.velocity = -20

        if self.rect.top <= 200:
            if self.velocity < 0:
                up = -dy

        self.rect.x += dx
        self.rect.y += dy + up

        if self.rect.top > 600:
            self.kill()

        return up

komar = Komar()
all_sprites.add(komar)


class GameStates(): # тело игры
    def __init__(self):
        self.state = 'intro'
        self.start = True
        self.limit = 15
        self.switch = True
        self.h = 350
        self.island = Islands(200, 440)
        platforms.add(self.island)
        self.fumigator = Fumigator(-40, 250)
        self.num_y1 = 150

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'

        pygame.display.flip()

    def main_game(self):
        userInput = pygame.key.get_pressed()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.start = False
            if userInput[pygame.K_RCTRL] or userInput[pygame.K_LCTRL]:
                f = open("scores.txt", "r")
                a = f.readlines()
                if len(a) == 0 or (len(a) == 1 and a[0] == "\n"):
                    result = '1 result:' + str(komar.score)
                    f = open("scores.txt", "a")
                    f.write(result + '\n')
                    f.close()
                else:
                    f = open("scores.txt", "r")
                    num = f.readlines()
                    f = open("scores.txt", "a")
                    cnt = int(num[-1][0]) + 1
                    result = str(cnt) + ' result:' + str(komar.score)
                    f.write(result + '\n')
                    f.close()
        up = komar.play(self.start)
        if len(all_sprites) == 1:
            screen.blit(background, (0, 0))
            all_sprites.draw(screen)
            platforms.draw(screen)
            fumigator.draw(screen)
            if len(platforms) < self.limit:
                self.island = Islands(random.randint(-100, 350), self.island.rect.y - random.randint(140, 155))
                platforms.add(self.island)
                self.fumigator = Fumigator(random.randint(-100, 650), self.fumigator.rect.y - 300)
                fumigator.add(self.fumigator)
                self.num_y1 -= 150
            platforms.update(up)
            fumigator.update(up)
        else:
            komar.kill()
            platforms.empty()
            end_screen(komar.score)
        pygame.display.flip()

    def state_image(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()


game_state = GameStates()


def start_screen(): # стартовое окно
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


def end_screen(final_score): # конечное окно
    global gr, x, y
    global game_score
    screen.fill((0, 0, 0))
    intro_text = ["score: ", str(final_score),
                  "from Zhamilya and Dameli", "", "", "", "",
                  "", "", "", "", "",
                  "thanks!", "", "Для записи результата нажмите CTRL"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(pygame.transform.scale(fon, [200, 200]), (150, 150))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for i in intro_text:
        text_welcome = font.render(i, True, (255, 255, 255))
        intro_rect = text_welcome.get_rect()
        intro_rect.center = (500, 0)
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(text_welcome, intro_rect)

    pygame.display.update()


start_screen()
while True:
    game_state.state_image()

