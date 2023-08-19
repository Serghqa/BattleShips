import pygame
import init_pole

pygame.init()

pole = init_pole.Pole()  # создаем объект для расстановки кораблей на игровом поле
pole.arrangement()  # расставляем корабли на поле

WIDTH = 400  # ширина поля
HEIGHT = 400  # высота поля
WHITE = (255, 255, 255)  # константа белого цвета
BLUE = (0, 0, 255)  # константа голубого цвета
BLACK = (0, 0, 0)  # константа черного цвета
RED = (255, 0, 0)  # константа красного цвета
GREY = (160, 160, 160)  # константа серого цвета
GREEN = (0, 255, 0)
FPS = 30  # переменная кадров в секунду
RUNNING = True  # флаг для остановки основного цикла событий
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # игровое окно (ширина, высота)

pygame.display.set_caption('BattleShips')  # название игры в консоли игрового окна
pygame.display.set_icon(pygame.image.load('battle.bmp'))  # иконка в консоли игрового окна
objects_deck = []  # список для хранения координат подбитых палуб
object_past = []  # список для хранения координат куда мы уже стреляли

def set_menu():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(WHITE)
    text = pygame.font.SysFont('arial', 22)
    sc_text = text.render('Выберите уровень сложности', 1, RED, WHITE)
    pos = sc_text.get_rect(center=(WIDTH//2, HEIGHT//6))
    sc_1 = text.render('Нажмите 1, если хотите выбрать 30 ходов', 1, RED, WHITE)
    pos_1 = sc_1.get_rect(center=(WIDTH//2, HEIGHT//3))
    sc_2 = text.render('Нажмите 2, если хотите выбрать 50 ходов', 1, RED, WHITE)
    pos_2 = sc_2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surf.blit(sc_text, pos)
    surf.blit(sc_1, pos_1)
    surf.blit(sc_2, pos_2)
    sc.blit(surf, (0, 0))
    pygame.display.update()


def win():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(GREEN)
    text = pygame.font.SysFont('arial', 30)
    text_win = text.render('Поздравляем!', 1, BLUE, GREEN)
    pos = text_win.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    surf.blit(text_win, pos)
    sc.blit(surf, (0, 0))
    pygame.display.update()


def lost():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(RED)
    text = pygame.font.SysFont('arial', 30)
    text_win = text.render('Вы проиграли!', 1, BLACK, RED)
    pos = text_win.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    surf.blit(text_win, pos)
    sc.blit(surf, (0, 0))
    pygame.display.update()


def set_lines(coor_x, coor_y, obj=None, flag=None):  # функция для отрисовки событий на игровом поле
    sc.fill(BLACK)  # заливка игрового поля цветом
    if obj:
        if flag:
            objects_deck.append(obj)  # добавляем координату подбитой палубы
        else:
            object_past.append(obj)  # добавляем координату выстрела мимо корабля
    for x in range(0, HEIGHT, HEIGHT // 10):
        pygame.draw.line(sc, BLUE, (0, x), (WIDTH, x))  # отрисовка горизонтальных линий поля
    for x in range(0, WIDTH, WIDTH // 10):
        pygame.draw.line(sc, BLUE, (x, 0), (x, HEIGHT))  # отрисовка вертикальных линий
    pygame.draw.line(sc, BLUE, (0, HEIGHT), (WIDTH, HEIGHT), 4)  # крайняя нижняя линия поля
    pygame.draw.line(sc, BLUE, (WIDTH, 0), (WIDTH, HEIGHT), 4)  # крайняя правая линия
    pygame.draw.rect(sc, WHITE, (coor_x, coor_y, WIDTH // 10, HEIGHT // 10), 5)  # рисуем квадратный курсор
    if len(objects_deck):
        for k in objects_deck:
            n, m = k[0], k[1]
            pygame.draw.rect(sc, RED, (n, m, WIDTH // 11, HEIGHT // 11))  # отображаем на игровом поле подбитую палубу
    if len(object_past):
        for k in object_past:
            n, m = k[0], k[1]
            pygame.draw.rect(sc, GREY, (n, m, WIDTH // 11, HEIGHT // 11))  # отображаем на игровом поле выстрел мимо

def find_ship(x, y):  # функция поиска корабля по координате игрового поля
    for ship in pole.ships_pole:
        if any(filter(lambda c: c == (y, x), ship.cell)):
            return ship  # возвращаем корабль, которому принадлежит данная координата


clock = pygame.time.Clock()  # объект для создания ограничения кадров в секунду (FPS)

x = 0  # координата движения курсора на игровом поле (движение по горизонтали)
y = 0  # координата движения курсора на игровом поле (движение по вертикали)
speed = WIDTH // 10  # скорость движения курсора
coord_x = 0  # инициализация координаты для сравнения координаты курсора на поле с координатой расположения корабля
coord_y = 0  # инициализация координаты для сравнения координаты курсора на поле с координатой расположения корабля
stage = 0

while RUNNING:
    set_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                stage = 1
                RUNNING  = False
            if event.key == pygame.K_2:
                stage = 2
                RUNNING = False

RUNNING = True
moves = {1: 30, 2: 50}[stage]
set_lines(coord_x, coord_y)  # рисуем поле

while RUNNING:  # пока RUNNING == True, цикл не закончится
    if moves == 0:
        lost()
    for event in pygame.event.get():  # перебор событий после одного цикла
        if event.type == pygame.QUIT:  # если событие == 'закрыть окно', RUNNING = False и основной цикл закончится
            RUNNING = False
        elif event.type == pygame.KEYDOWN:  # проверка нажатия клавиши на клавиатуре
            if event.key == pygame.K_LEFT:  # нажата клавиша 'стрелка влево'
                if x > 0:  # проверяем выход за границы игрового поля
                    x -= speed  # сдвигаем курсор влево на заданную величину
                    coord_x -= 1  # смещаем координату для поиска в соответствии с координатой курсора
                    set_lines(x, y)  # перерисовываем поле с новыми координатами курсора
            elif event.key == pygame.K_RIGHT:
                if x < WIDTH - speed:
                    x += speed
                    coord_x += 1
                    set_lines(x, y)
            elif event.key == pygame.K_UP:
                if y > 0:
                    y -= speed
                    coord_y -= 1
                    set_lines(x, y)
            elif event.key == pygame.K_DOWN:
                if y < HEIGHT - speed:
                    y += speed
                    coord_y += 1
                    set_lines(x, y)
            elif event.key == pygame.K_SPACE:  # нажата клавиша 'пробел'
                moves -= 1
                if pole.pole[coord_y][coord_x] == '*':  # проверка на попадание по кораблю
                    pole.pole[coord_y][coord_x] = 1  # изменение значения после попадания по кораблю
                    ship = find_ship(coord_x, coord_y)  # поиск корабля по координате
                    ship.counter -= 1  # уменьшение очков прочности корабля
                    if ship.counter > 0:  # проверка прочности корабля
                        print('Ранил')
                    else:
                        pole.ships_pole.remove(ship)  # удаление корабля из списка если его прочность равна 0
                        print('Убил')
                        if len(pole.ships_pole) == 0:
                            win()
                    set_lines(x, y, (x, y), True)  # перерисовка всего поля с новыми данными после события
                elif pole.pole[coord_y][coord_x] == 1:  # сообщение по повторной координате
                    print('Уже стреляли')
                else:
                    print('Мимо')
                    set_lines(x, y, (x, y), False)  # отрисовка игрового поля после промаха
                for i in pole.pole:
                    print(*i)
    clock.tick(FPS)  # создаём ограничение кадров в секунду (число итераций в секунду за один цикл while)

    pygame.display.update()  # буферизация изображения на клиентской области окна

print('version_1.0')