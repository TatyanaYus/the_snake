from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POINT = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет камня - не съедобная еда
STONE_COLOR = (101, 67, 33)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка. Выход: ESC.')


# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс.
    От него наследуются другие игровый объекты (цвет объекта и позицию).
    """

    def __init__(self, body_color=(0, 0, 0), position=CENTER_POINT):
        """Инициализирует базовые атрибуты объекта (цвет и позиция)."""
        self.body_color = body_color
        self.position = position
        self.border_color = body_color

    def draw(self, position=None):
        """
        Абстрактный метод.
        Предназначен для переопределения в дочерних классах.
        """
        if position is None:
            position = self.position
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

        # raise NotImplementedError


class Apple(GameObject):
    """
    Класс наследуется от GameObject.
    Описывает яблоко (цвет) и действие с ним (позиция яблока на игровом поле).
    Определяет как объект отрисовывается на экране.
    """

    def __init__(self, body_color=APPLE_COLOR, position=(0, 0),
                 occupied_cells=[]):
        """Задает цвет яблока. Вызывает метод randomize_position."""
        super().__init__(body_color, position)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """
        Устанавливает случайное положение яблока на игровом поле,
        учитывая границы игрового поля.
        """
        self.position = None
        while self.position is None or self.position in occupied_cells:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Stone(Apple):
    """
    Класс наследуется от Apple.
    Описывает камень (цвет) - не съедобную объект и действия с ним
    (позицию камня на игровом поле).
    Определяет как объект отрисовывается на экране.
    """


class Snake(GameObject):
    """
    Класс наследуется от GameObject. Описывает змейку (цвет) и ее поведение.
    Управляет движением змейки, отрисовкой,
    обрабатывает действия пользователя (нажатие клавиши).
    """

    def __init__(self, body_color=SNAKE_COLOR, position=CENTER_POINT):
        """
        Инициализирует начальное состояние змейки.
        positions - список, содержащий позиции всех сегментов тела змейки.
        direction - направление движения.
        last - хранит позицию последнего сегмента змейки перед
        его исчезновением (при движении змейки).
        """
        super().__init__(body_color, position)
        self.reset()
        self.direction = RIGHT
        self.border_color = BORDER_COLOR
        self.last = None
        self.pre_last = None

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции)."""
        x, y = self.get_head_position()
        new_head = ((x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                    (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)

        self.last, self.pre_last = None, None
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()
        if len(self.positions) > self.lenght:
            self.pre_last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[1:]:
            super().draw(position)

        # Отрисовка головы змейки
        super().draw(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            if self.pre_last:
                pre_last_rect = pg.Rect(
                    self.pre_last, (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, pre_last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.lenght = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш и изменяет направление движения змейки."""
    keyboard = {
        (LEFT, pg.K_UP): UP,
        (LEFT, pg.K_DOWN): DOWN,
        (RIGHT, pg.K_UP): UP,
        (RIGHT, pg.K_DOWN): DOWN,
        (UP, pg.K_LEFT): LEFT,
        (UP, pg.K_RIGHT): RIGHT,
        (DOWN, pg.K_LEFT): LEFT,
        (DOWN, pg.K_RIGHT): RIGHT
    }

    for event in pg.event.get():
        if (event.type == pg.QUIT
                or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            return False
        if event.type == pg.KEYDOWN:
            new_direction = keyboard.get(
                (game_object.direction, event.key), game_object.direction)
            game_object.update_direction(new_direction)

    return True


def main():
    """В основном цикле игры обновляется состояние объектов."""
    # Инициализация PyGame:
    pg.init()
    speed = SPEED
    snake = Snake(SNAKE_COLOR)
    apple = Apple(occupied_cells=snake.positions)
    stone = Stone(body_color=STONE_COLOR,
                  occupied_cells=snake.positions + [apple.position])

    while True:
        """
        Змейка обрабатывает нажатие клавиш и двигается в соответсвии с
        выбранным направлением.
        Если змейка съедает яблоко ее размер увеличивается на один сегмент,
        а яблоко перемещается в новую случайную позицию.
        При столкновении змейки с самой собой игра начинается заново.
        Игра продолжается, пока пользователь не закроет окно.
        """
        clock.tick(speed)
        if not handle_keys(snake):
            break

        snake.move()

        # Если змея съела яблоко
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            speed += 1
            apple.randomize_position(snake.positions + [stone.position])

        # Если змея съела камень, то ее размер уменьшается на 1
        # Если размер змейки был 1 и змейка съела камень - игра обнуляется
        if snake.get_head_position() == stone.position:
            if snake.lenght == 1:
                screen.fill(BOARD_BACKGROUND_COLOR)
                snake.reset()
                speed = SPEED
            else:
                snake.lenght -= 1
                speed -= 1
            stone.randomize_position(snake.positions + [apple.position])

        # Если змея ударилась об себя
        if snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            speed = SPEED

        snake.draw()
        apple.draw()
        stone.draw()
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main()
