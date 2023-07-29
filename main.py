import pygame

pygame.init()

WIDTH = 400  # ширина поля
HEIGHT = 400  # высота поля
WHITE = (255, 255, 255)  # константа белого цвета
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 30  # переменная кадров в секунду
RUNNING = True  # флаг для остановки основного цикла событий
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # игровое окно (ширина, высота)

pygame.display.set_caption('BattleShips')  # название игры в консоли игрового окна
pygame.display.set_icon(pygame.image.load('battle.bmp'))  # иконка в консоли игрового окна

def set_lines():
    sc.fill(BLACK)
    for x in range(0, HEIGHT, HEIGHT // 10):
        pygame.draw.line(sc, BLUE, (0, x), (WIDTH, x))  # отрисовка горизонтальных линий поля
    for x in range(0, WIDTH, WIDTH // 10):
        pygame.draw.line(sc, BLUE, (x, 0), (x, HEIGHT))  # отрисовка вертикальных линий
    pygame.draw.line(sc, BLUE, (0, HEIGHT), (WIDTH, HEIGHT), 4)  # крайняя нижняя линия поля
    pygame.draw.line(sc, BLUE, (WIDTH, 0), (WIDTH, HEIGHT), 4)  # крайняя правая линия


clock = pygame.time.Clock()  # объект для создания ограничения кадров в секунду (FPS)

x = 0
y = 0
speed = WIDTH // 10


while RUNNING:  # пока RUNNING == True, цикл не закончится
    for event in pygame.event.get():  # перебор событий после одного цикла
        if event.type == pygame.QUIT:  # если событие == 'закрыть окно', RUNNING = False и основной цикл закончится
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x > 0:
                    x -= speed
            elif event.key == pygame.K_RIGHT:
                if x < WIDTH - speed:
                    x += speed
            elif event.key == pygame.K_UP:
                if y > 0:
                    y -= speed
            elif event.key == pygame.K_DOWN:
                if y < HEIGHT - speed:
                    y += speed
    clock.tick(FPS)  # создаём ограничение кадров в секунду (число итераций в секунду за один цикл while)
    set_lines()
    pygame.draw.rect(sc, WHITE, (x, y, WIDTH//10, HEIGHT//10), 5)
    pygame.display.update()  # буферизация изображения на клиентской области окна



