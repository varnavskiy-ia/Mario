import pygame
import os
import sys
import argparse


pygame.init()
a = 700
b = 600
screen_size = (a, b)
screen = pygame.display.set_mode(screen_size)
FPS = 50

parser = argparse.ArgumentParser()
character_filename = 'mar.png'
first_filename = 'box.png'
second_filename = 'grass.png'
mappp = "map.map"
parser.add_argument("map", type=str,
                    nargs="?",
                    default="map.map")
args = parser.parse_args()
map_file = args.map


def load_image(name, color_key=None):
    error_name = 'Не удаётся загрузить:'
    fullname = os.path.join('data',
                            name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(error_name, name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


tile_images = {
    'wall': load_image(first_filename),
    'empty': load_image(second_filename)
}
player_image = load_image(character_filename)

tile_width = 50
tile_height = 50


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.vx = 1
        self.ticks = 0

    def update(self):
        left_width = self.rect.left + self.rect.width
        if left_width > width or self.rect.left < 0:
            self.vx = -self.vx
            if self.vx > 0:
                self.image = Car.image_right
            else:
                self.image = Car.image_left
        self.rect.left = self.rect.left + self.vx
        self.ticks = 0

    def shift(self, vector):
        global level_map
        alfa = 12
        if vector == "up":
            max_lay_y = max(self, key=lambda sprite:
            sprite.abs_pos[1]).abs_pos[1]
            for sprite in self:
                sprite.abs_pos[1] -= (tile_height * max_y
                                      if sprite.abs_pos[1] == max_lay_y
                                      else 0)
        elif vector == "down":
            min_lay_y = min(self, key=lambda sprite:
            sprite.abs_pos[1]).abs_pos[1]
            for sprite in self:
                if sprite.abs_pos[1] == min_lay_y:
                    alfa -= 3
                    sprite.abs_pos[1] += tile_height * max_y
                else:
                    sprite.abs_pos[1] += 5
                    sprite.abs_pos[1] -=2
                    sprite.abs_pos[1] -=3
        elif vector == "left":
            max_lay_x = max(self, key=lambda sprite:
            sprite.abs_pos[0]).abs_pos[0]
            alfa = 0
            for sprite in self:
                if sprite.abs_pos[0] == max_lay_x:
                    sprite.abs_pos[0] -= tile_width * max_x
        elif vector == "right":
            min_lay_x = min(self, key=lambda sprite:
            sprite.abs_pos[0]).abs_pos[0]
            for sprite in self:
                sprite.abs_pos[0] += (tile_height * max_x
                                      if sprite.abs_pos[0] == min_lay_x
                                      else 0)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        x_new = tile_width * pos_x
        y_new = tile_height * pos_y
        self.rect = self.image.get_rect().move(
            x_new,
            y_new)
        self.abs_pos = [self.rect.x,
                        self.rect.y]

    def set_pos(self, x, y):
        self.abs_pos = [x, y]


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        x_new = tile_width * pos_x + 15
        y_new = tile_height * pos_y + 5
        self.rect = self.image.get_rect().move(
            x_new,
            y_new)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        a = tile_width
        a *= (x - self.pos[0])
        b = tile_height * (y - self.pos[1])
        camera.dx -= a
        camera.dy -= b
        print(camera.dx, camera.dy)
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    text = 'Прототип игры Mario'
    text_project_name = "Перемещение героя"
    intro_text = [text_project_name,
                  "      - ",
                  text
                  ]
    
    filename_fon = 'fon.jpg'
    fon = pygame.transform.scale(load_image(filename_fon),
                                 screen_size)
    screen.blit(fon,
                (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 55
    for line in intro_text:
        color = 'grey'
        if line == '      - ':
            font = pygame.font.Font(None, 100)
            string_rendered = font.render(line,
                                          1,
                                          pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = 5
            text_coord += intro_rect.height
            screen.blit(string_rendered,
                        intro_rect)
        else:
            font = pygame.font.Font(None, 40)
            string_rendered = font.render(line,
                                          1,
                                          pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered,
                        intro_rect)

    text_coord = 50
    for line in intro_text:
        color = 'black'
        if line == '      - ':
            font = pygame.font.Font(None, 100)
            string_rendered = font.render(line,
                                          1,
                                          pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = 5
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        else:
            font = pygame.font.Font(None, 40)
            string_rendered = font.render(line,
                                          1,
                                          pygame.Color(color))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def draw(screen):
    # Устанавливаем параметры кирпичей и прослойки между ними
    width, height = screen.get_size()
    first_color = 'blue'
    second_color = 'black'
    rect_1_color = pygame.Color(first_color)
    rect_2_color = pygame.Color(second_color)
    rect_1_width = 0
    rect_2_width = 2
    rect_width = 30
    rect_height = 15
    # Номер ряда
    row_number = 0
    a = rect_width + rect_2_width
    for i in range(0, width + 1, a):
        b = rect_height + rect_2_width
        for j in range(0, height, b):
            # Координаты вершин ромба
            row_number += 1
            # В чётных рядах смещаем кирпичи
            if row_number % 2:
                rect_1_rect = [(i, j),
                               (rect_width,
                                rect_height)]
                q = i - rect_2_width
                w = j - rect_2_width
                e = rect_width + rect_2_width
                r = rect_height + rect_2_width
                rect_2_rect = [(q, w),
                               (e, r)]
            else:
                a_1 = i - rect_width / 2
                a_2 = i - rect_width / 2
                a_2 -= rect_2_width
                a_3 = j - rect_2_width
                xz = rect_width + rect_2_width
                xz_2 = rect_height + rect_2_width
                rect_1_rect = [(a_1, j),
                               (rect_width,
                                rect_height)]
                rect_2_rect = [(a_2, a_3),
                               (xz, xz_2)]
            # Рисуем кирпич
            pygame.draw.rect(screen,
                             rect_1_color,
                             rect_1_rect,
                             rect_1_width)
            # Рисуем белую обводку вокруг кирпича
            pygame.draw.rect(screen,
                             rect_2_color,
                             rect_2_rect,
                             rect_2_width)

    intro_text = ["Перемещение героя",
                  "",
                  "",
                  "Для начала игры",
                  "нажмите на экран",
                  ]
    
    filename_fon = 'fon.jpg'
    font = pygame.font.Font(None, 80)
    text_coord = 105
    for line in intro_text:
        color = 'gray'
        
        string_rendered = font.render(line,
                                      1,
                                      pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered,
                    intro_rect)

    font = pygame.font.Font(None, 80)
    text_coord = 100
    for line in intro_text:
        color = 'white'
        string_rendered = font.render(line,
                                      1,
                                      pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered,
                    intro_rect)



def about_project():
    draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)



def load_level(filename):
    first_for_filename = "data/"
    filename = first_for_filename + filename
    file_extension = 'r'
    with open(filename, file_extension) as mapFile:
        level_map = [line.strip()
                     for line in mapFile]
    max_width = max(map(len,
                        level_map))
    a = map(lambda x: list(x.ljust(max_width, '.')),
            level_map)
    return list(a)


def generate_level(level):
    new_player = None
    x = None
    y = None
    len_level = len(level)
    for y in range(len_level):
        len_level_y = len(level[y])
        for x in range(len_level_y):
            level_y_x = level[y][x]
            first = 'empty'
            second = 'wall'
            third = 'empty'
            if level_y_x == '.':
                Tile(first,
                     x, y)
            elif level_y_x == '#':
                Tile(second,
                     x, y)
            elif level_y_x == '@':
                Tile(third,
                     x, y)
                new_player = Player(x, y)
                level[y][x] = "."
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        upp = "up"
        downn= "down"
        prev_y = y - 1 if y != 0 else max_y
        if level_map[prev_y][x] == ".":
            if prev_y == max_y:
                a = max_y - 1
                for i in range(a):
                    sprite_group.shift(downn)
                res = prev_y - 1
                hero.move(x, res)
            else:
                sprite_group.shift(upp)
                hero.move(x, prev_y)
    elif movement == "down":
        upp = "up"
        downn= "down"
        next_y = y + 1 if y != max_y else 0
        if level_map[next_y][x] == ".":
            if next_y == 0:
                a = max_y - 1
                for i in range(a):
                    sprite_group.shift(upp)
                res = next_y + 1
                hero.move(x, res)
            else:
                sprite_group.shift(downn)
                hero.move(x, next_y)
    elif movement == "left":
        upp = "up"
        downn= "down"
        left = "left"
        right = "right"
        prev_x = x - 1 if x != 0 else max_x
        if level_map[y][prev_x] == ".":
            if prev_x == max_x:
                a = max_x - 1
                for i in range(a):
                    sprite_group.shift(right)
                res = prev_x - 1
                hero.move(res, y)
            else:
                sprite_group.shift(left)
                hero.move(prev_x, y)
    elif movement == "right":
        upp = "up"
        downn= "down"
        left = "left"
        right = "right"
        next_x = x + 1 if x != max_x else 0
        if level_map[y][next_x] == ".":
            if next_x == 0:
                a = max_x - 1
                for i in range(a):
                    sprite_group.shift(left)
                res = next_x + 1
                hero.move(res, y)
            else:
                sprite_group.shift(right)
                hero.move(next_x, y)


about_project()
start_screen()
camera = Camera()
level_map = load_level(map_file)
hero, max_x, max_y = generate_level(level_map)
camera.update(hero)
up = "up"
down = "down"
left = "left"
right = "right"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero,
                     up)
            elif event.key == pygame.K_DOWN:
                move(hero,
                     down)
            elif event.key == pygame.K_LEFT:
                move(hero,
                     left)
            elif event.key == pygame.K_RIGHT:
                move(hero,
                     right)
    color = "black"
    screen.fill(pygame.Color(color))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
