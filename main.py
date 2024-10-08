import pygame
import random
import time

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 896
SCREEN_HEIGHT = 512
FPS = 60

background = pygame.image.load('imgs/backg.png')
bot_front = pygame.image.load('imgs/bot_f.png')
bot_left = pygame.image.load('imgs/bot_l.png')
bot_right = pygame.image.load('imgs/bot_r.png')
r_light = pygame.image.load('imgs/r_light.png')

pygame.mixer.music.load("music/floppy-disks.mp3")
# Музыка: Floppy Disks by Shane Ivers - https://www.silvermansound.com
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

bot_width, bot_height = bot_front.get_size()    # Получает размер персонажа из переменной которая хранит bot_f.png
bot_y_offset = 20                               # Подъём на 20 пикселей от низа экрана

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ДиДос.exexe')

clock = pygame.time.Clock()                             # Устанавливаю таймер

character_x = (SCREEN_WIDTH - bot_width) // 2           # Ставлю бота по центру, по горизонтали
character_y = SCREEN_HEIGHT - bot_height - bot_y_offset
character_speed = 5                                     # Задаю скорость движения бота
character_img = bot_front                               # Назначаю изображения бота по умолчанию

red_lights = []                 # Красные огоньки
red_light_speed = 5             # Скорость красных огоньков

start_time = time.time()        # Запускаю таймер

game_over = False               # Условия окончания игры сейчас имеют бул. значение False

font = pygame.font.SysFont('CrystalRevived', 36)        # Настраиваю шрифт

def create_red_light():                                            # Создание огоньков
    x = random.randint(0, SCREEN_WIDTH - r_light.get_width())   # В случайном месте по горизонтали
    y = -r_light.get_height()                                      # За верхней границей экрана
    return [x, y]

def check_collision(rect1, rect2):      # Проверка столкновения "хитбоксов"
    return rect1.colliderect(rect2)     # Через colliderect

def draw_game_over_screen(final_time):  # Рисует окно окончания игры, принимает аргумент
    screen.fill((0, 0, 0))              # Очистка экрана
    game_over_text = font.render(f"Сервер упал! Вы продержалисб: {final_time:.2f} секундов!", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(10000)             # Задержка 10 секунд

# ГЛАВНЫЙ ЦИКЛ
while True:
    if not game_over:
        # Пока игра не закончена, идёт подсчёт продолжительности игровой сессии
        elapsed_time = time.time() - start_time

        # Стандартный модуль корректного закрытия игры при закрытии главного окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # УПРАВЛЕНИЕ
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= character_speed
            character_img = bot_left        # Вызывает картинку движения бота влево
        elif keys[pygame.K_RIGHT]:
            character_x += character_speed
            character_img = bot_right       # Вызывает картинку движения бота вправо
        else:
            character_img = bot_front       # Когда бот стоит, он отображается как bot_f.png

        # Сдерживание бота в границах экрана
        if character_x < 0:
            character_x = 0
        elif character_x > SCREEN_WIDTH - bot_width:
            character_x = SCREEN_WIDTH - bot_width

        # Обновление движения (позиции) огоньков
        for light in red_lights:
            light[1] += red_light_speed

        # Удаление огоньков достигший низа экрана
        red_lights = [light for light in red_lights if light[1] < SCREEN_HEIGHT]

        # Проверка столкновений
        character_rect = pygame.Rect(character_x, character_y, bot_width, bot_height)
        for light in red_lights:
            light_rect = pygame.Rect(light[0], light[1], r_light.get_width(), r_light.get_height())
            if check_collision(character_rect, light_rect):
                game_over = True
                final_time = elapsed_time

        # Добавление огоньков
        if random.randint(1, 60) == 1:
            red_lights.append(create_red_light())

        # ПОЛНАЯ ОТРИСОВКА
        screen.blit(background, (0, 0))
        screen.blit(character_img, (character_x, character_y))
        for light in red_lights:
            screen.blit(r_light, (light[0], light[1]))

        pygame.display.flip()

        clock.tick(FPS)
    else:                                   # В противном случае выводим экран окончания игры
        draw_game_over_screen(final_time)   # со значением продолжительности игровой сессии
        pygame.quit()
        exit()
