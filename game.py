import pygame
import init_pole

pygame.init()
pole = init_pole.Pole()  # создаем объект для расстановки кораблей на игровом поле

# размеры окна
WIDTH = 600  # ширина окна
HEIGHT = 400  # высота окна
# размеры игрового поля
W_POLE = 400
H_POLE = 400

# константы цветов
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (160, 160, 160)
GREEN = (0, 255, 0)

FPS = 30  # переменная кадров в секунду
RUNNING = True  # флаг для остановки основного цикла событий

sc = pygame.display.set_mode((WIDTH, HEIGHT))  # игровое окно (ширина, высота)

x = 0  # координата движения курсора на игровом поле (движение по горизонтали)
y = 0  # координата движения курсора на игровом поле (движение по вертикали)

speed = W_POLE // 10  # скорость движения курсора
coord_x = 0  # инициализация координаты для сравнения координаты курсора на поле с координатой расположения корабля
coord_y = 0  # инициализация координаты для сравнения координаты курсора на поле с координатой расположения корабля

moves_stage = {1: 30, 2: 50}  # константа определения количества ходов
moves = 1
stage = 1
START = True  # константа определения вызова меню

name = 'BattleShips'
pygame.display.set_caption(name)  # название игры в консоли игрового окна
pygame.display.set_icon(pygame.image.load('battle.bmp'))  # иконка в консоли игрового окна
objects_deck = []  # список для хранения координат подбитых палуб
object_past = []  # список для хранения координат куда мы уже стреляли


def set_menu():  # функция выбора количества ходов в меню перед началом игры
    global objects_deck
    global object_past
    global pole
    global RUNNING
    global moves_stage
    global moves
    global stage
    global START
    while START:
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill(BLACK)
        text = pygame.font.SysFont('arial', 22)
        sc_text = text.render('Выберите уровень сложности', 1, RED, BLACK)
        pos = sc_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        sc_1 = text.render('Нажмите 1, если хотите выбрать 30 ходов', 1, RED, BLACK)
        pos_1 = sc_1.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        sc_2 = text.render('Нажмите 2, если хотите выбрать 50 ходов', 1, RED, BLACK)
        pos_2 = sc_2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surf.blit(sc_text, pos)
        surf.blit(sc_1, pos_1)
        surf.blit(sc_2, pos_2)
        sc.blit(surf, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                START = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    stage = 1
                    pole.__init__()
                    pole.arrangement()  # расставляем корабли на поле
                    objects_deck = []  # список для хранения координат подбитых палуб
                    object_past = []  # список для хранения координат куда мы уже стреляли
                    moves = moves_stage[stage]  # количество ходов
                    START = False
                if event.key == pygame.K_2:
                    stage = 2
                    pole.__init__()
                    pole.arrangement()  # расставляем корабли на поле
                    objects_deck = []  # список для хранения координат подбитых палуб
                    object_past = []  # список для хранения координат куда мы уже стреляли
                    moves = moves_stage[stage]  # количество ходов
                    START = False


def menu_stage(moves, ships, ev=None):  # текстовое меню количества ходов и кораблей
    surf = pygame.Surface((WIDTH - W_POLE, HEIGHT))
    surf.fill(BLACK)
    if ev:
        text_event = pygame.font.SysFont('arial', 22)
        sc_text_event = text_event.render(ev, 1, RED, BLACK)
        pos_text_event = sc_text_event.get_rect(center=(100, 100))
        surf.blit(sc_text_event, pos_text_event)

    text_ships = pygame.font.SysFont('arial', 22)
    sc_ships_text = text_ships.render(f'Кораблей осталось {str(ships)}', 1, RED, BLACK)
    pos_ships = sc_ships_text.get_rect(center=(100, 200))
    surf.blit(sc_ships_text, pos_ships)

    text = pygame.font.SysFont('arial', 22)
    sc_text = text.render(f'Ходов {moves}', 1, RED, BLACK)
    pos = sc_text.get_rect(center=(100, 50))
    surf.blit(sc_text, pos)
    sc.blit(surf, (W_POLE, 0))
    pygame.display.update()


def win():  # меню после победы
    global RUNNING
    global START
    while not START:
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill(GREEN)
        text = pygame.font.SysFont('arial', 30)
        text_win = text.render('Поздравляем!', 1, BLUE, GREEN)
        pos = text_win.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        text_restart = text.render('Начать заново - жми 1', 1, BLUE, GREEN)
        pos_restart = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        text_end = text.render('Закончить - жми 2', 1, BLUE, GREEN)
        pos_end = text_end.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surf.blit(text_restart, pos_restart)
        surf.blit(text_end, pos_end)
        surf.blit(text_win, pos)
        sc.blit(surf, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                START = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    START = True
                elif event.key == pygame.K_2:
                    RUNNING = False
                    START = True


def lost():  # меню после проигрыша
    global RUNNING
    global START
    while not START:
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill(RED)
        text = pygame.font.SysFont('arial', 30)
        text_win = text.render('Вы проиграли!', 1, BLACK, RED)
        pos = text_win.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        text_restart = text.render('Начать заново - жми 1', 1, BLACK, RED)
        pos_restart = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        text_end = text.render('Закончить - жми 2', 1, BLACK, RED)
        pos_end = text_end.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surf.blit(text_restart, pos_restart)
        surf.blit(text_end, pos_end)
        surf.blit(text_win, pos)
        sc.blit(surf, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                START = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    START = True
                elif event.key == pygame.K_2:
                    RUNNING = False
                    START = True


def set_lines(coor_x, coor_y, obj=None, flag=None):  # функция для отрисовки событий на игровом поле
    sc.fill(BLACK)  # заливка игрового поля цветом
    if obj:
        if flag:
            objects_deck.append(obj)  # добавляем координату подбитой палубы
        else:
            object_past.append(obj)  # добавляем координату выстрела мимо корабля
    for x in range(0, H_POLE, H_POLE // 10):
        pygame.draw.line(sc, BLUE, (0, x), (W_POLE, x))  # отрисовка горизонтальных линий поля
    for x in range(0, W_POLE, W_POLE // 10):
        pygame.draw.line(sc, BLUE, (x, 0), (x, H_POLE))  # отрисовка вертикальных линий
    pygame.draw.line(sc, BLUE, (0, H_POLE), (W_POLE, H_POLE), 4)  # крайняя нижняя линия поля
    pygame.draw.line(sc, BLUE, (W_POLE, 0), (W_POLE, H_POLE), 4)  # крайняя правая линия
    pygame.draw.rect(sc, WHITE, (coor_x, coor_y, W_POLE // 10, H_POLE // 10), 5)  # рисуем квадратный курсор
    if len(objects_deck):
        for k in objects_deck:
            n, m = k[0], k[1]
            pygame.draw.rect(sc, RED, (n, m, W_POLE // 11, H_POLE // 11))  # отображаем на игровом поле подбитую палубу
    if len(object_past):
        for k in object_past:
            n, m = k[0], k[1]
            pygame.draw.rect(sc, GREY, (n, m, W_POLE // 11, H_POLE // 11))  # отображаем на игровом поле выстрел мимо


def find_ship(x, y):  # функция поиска корабля по координате игрового поля
    for ship in pole.ships_pole:
        if any(filter(lambda c: c == (y, x), ship.cell)):
            return ship  # возвращаем корабль, которому принадлежит данная координата


clock = pygame.time.Clock()  # объект для создания ограничения кадров в секунду (FPS)
set_lines(coord_x, coord_y)  # рисуем поле

while RUNNING:  # пока RUNNING == True, цикл не закончится
    if START:
        set_menu()
        x = 0  # координата движения курсора на игровом поле (движение по горизонтали)
        y = 0  # координата движения курсора на игровом поле (движение по вертикали)
        speed = W_POLE // 10  # скорость движения курсора
        coord_x = 0  # инициализация координаты для сравнения координаты курсора на поле с координатой расположения корабля
        coord_y = 0  # инициализация координаты для сравнения координаты курсора на поле с координатой расположения корабля
        sc = pygame.display.set_mode((WIDTH, HEIGHT))  # игровое окно (ширина, высота)
        set_lines(coord_x, coord_y)  # рисуем поле
        menu_stage(moves, len(pole.ships_pole))
        pygame.display.update()
    if moves == 0:
        lost()
    if len(pole.ships_pole) == 0:
        win()
    for event in pygame.event.get():  # перебор событий после одного цикла
        if event.type == pygame.QUIT:  # если событие == 'закрыть окно', RUNNING = False и основной цикл закончится
            RUNNING = False
        elif event.type == pygame.KEYDOWN:  # проверка нажатия клавиши на клавиатуре
            if event.key == pygame.K_LEFT:  # движение курсора влево
                if x > 0:  # проверяем выход за границы игрового поля
                    x -= speed  # сдвигаем курсор влево на заданную величину
                    coord_x -= 1  # смещаем координату для поиска в соответствии с координатой курсора
                    set_lines(x, y)  # перерисовываем поле с новыми координатами курсора
                    menu_stage(moves, len(pole.ships_pole))
            elif event.key == pygame.K_RIGHT:  # движение курсора вправо
                if x < W_POLE - speed:
                    x += speed
                    coord_x += 1
                    set_lines(x, y)
                    menu_stage(moves, len(pole.ships_pole))
            elif event.key == pygame.K_UP:  # движение курсора вверх
                if y > 0:
                    y -= speed
                    coord_y -= 1
                    set_lines(x, y)
                    menu_stage(moves, len(pole.ships_pole))
            elif event.key == pygame.K_DOWN:  # движение курсора вниз
                if y < HEIGHT - speed:
                    y += speed
                    coord_y += 1
                    set_lines(x, y)
                    menu_stage(moves, len(pole.ships_pole))
            elif event.key == pygame.K_SPACE:  # нажата клавиша 'пробел'
                if pole.pole[coord_y][coord_x] == '*':  # проверка на попадание по кораблю
                    moves -= 1
                    pole.pole[coord_y][coord_x] = 1  # изменение значения после попадания по кораблю
                    ship = find_ship(coord_x, coord_y)  # поиск корабля по координате
                    ship.counter -= 1  # уменьшение очков прочности корабля
                    if ship.counter > 0:  # проверка прочности корабля
                        print('Ранил')
                        ev = 'Ранил'
                    else:
                        pole.ships_pole.remove(ship)  # удаление корабля из списка если его прочность равна 0
                        print('Убил')
                        ev = 'Убил'
                    set_lines(x, y, (x, y), True)  # перерисовка всего поля с новыми данными после события
                    menu_stage(moves, len(pole.ships_pole), ev)
                elif pole.pole[coord_y][coord_x] == 1:  # сообщение по повторной координате
                    print('Уже стреляли')
                    ev = 'Уже стреляли'
                    menu_stage(moves, len(pole.ships_pole), ev)
                elif pole.pole[coord_y][coord_x] == 2:
                    print('Уже стреляли')
                    ev = 'Уже стреляли'
                    menu_stage(moves, len(pole.ships_pole), ev)
                else:
                    moves -= 1
                    pole.pole[coord_y][coord_x] = 2
                    print('Мимо')
                    ev = 'Мимо'
                    set_lines(x, y, (x, y), False)  # отрисовка игрового поля после промаха
                    menu_stage(moves, len(pole.ships_pole), ev)
                print(moves)
                for i in pole.pole:
                    print(*i)
    clock.tick(FPS)  # создаём ограничение кадров в секунду (число итераций в секунду за один цикл while)

    pygame.display.update()  # буферизация изображения на клиентской области окна

print('version_1.0')
