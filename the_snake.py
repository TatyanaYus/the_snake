from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс.
    От него наследуются другие игровый объекты (цвет объекта и позицию).
    """

    def __init__(self, body_color=(0, 0, 0), position=(0, 0)):
        """Инициализирует базовые атрибуты объекта (цвет и позиция)."""
        self.body_color = body_color
        self.position = position

    def draw(self):
        """
        Абстрактный метод.
        Предназначен для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс наследуется от GameObject.
    Описывает яблоко (цвет) и действие с ним (позиция яблока на игровом поле).
    Определяет как объект отрисовывается на экране.
    """

    def __init__(self, body_color=APPLE_COLOR, position=(0, 0)):
        """Задает цвет яблока. Вызывает метод randomize_position."""
        super().__init__(body_color, position)
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает случайное положение яблока на игровом поле,
        учитывая границы игрового поля.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, self.body_color, rect, 1)


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

    def __init__(self, body_color=SNAKE_COLOR, position=(0, 0)):
        """
        Инициализирует начальное состояние змейки.
        positions - список, содержащий позиции всех сегментов тела змейки.
        direction - направление движения.
        next_direction - следующее направление движения,
        применяется после обработки нажатия клавиши.
        last - хранит позицию последнего сегмента змейки перед
        его исчезновением (при движении змейки).
        """
        super().__init__(body_color, position)
        # lenght - длина змейки
        self.lenght = 1
        self.positions = [position]
        # direction - направление движения
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.lasts = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции)."""
        head = self.get_head_position()
        if self.direction == RIGHT:
            new_head = ((head[0] + RIGHT[0] * GRID_SIZE) %
                        SCREEN_WIDTH, head[1])
        elif self.direction == LEFT:
            new_head = ((head[0] + LEFT[0] * GRID_SIZE) %
                        SCREEN_WIDTH, head[1])
        elif self.direction == UP:
            new_head = (head[0], (head[1] + UP[1] * GRID_SIZE) % SCREEN_HEIGHT)
        else:
            new_head = (head[0], (head[1] + DOWN[1]
                        * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)

        self.last, self.lasts = None, None
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()
        if len(self.positions) > self.lenght:
            self.lasts = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            if self.lasts:
                lasts_rect = pygame.Rect(self.lasts, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, lasts_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш и изменяет направление движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def is_position_match(stone, apple, snake):
    """
    Обрабатывает граничные условия.
    Проверяет совпадение позиции камня, яблока и змейки.
    """
    while (stone.position == apple.position
           or apple.position in snake.positions
           or stone.position in snake.positions
           ):
        apple.position = apple.randomize_position()
        stone.position = stone.randomize_position()


def main():
    """В основном цикле игры обновляется состояние объектов."""
    # Инициализация PyGame:
    pygame.init()
    speed = SPEED
    apple = Apple(APPLE_COLOR, (0, 0))
    center_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    snake = Snake(SNAKE_COLOR, center_position)
    stone = Stone(STONE_COLOR, (0, 0))

    is_position_match(stone, apple, snake)

    snake.draw()
    apple.draw()
    stone.draw()
    pygame.display.update()

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
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Если змея съела яблоко
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            speed += 1
            apple.position = apple.randomize_position()

        # Если змея съела камень, то ее размер уменьшается на 1
        # Если размер змейки был 1 и змейка съела камень - конец игры
        if snake.get_head_position() == stone.position:
            if snake.lenght == 1:
                pygame.quit()
                raise SystemExit

            snake.lenght -= 1
            speed -= 1
            stone.position = stone.randomize_position()

            is_position_match(stone, apple, snake)

        # Если змея ударилась об себя
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            speed = SPEED

        snake.draw()
        apple.draw()
        stone.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
