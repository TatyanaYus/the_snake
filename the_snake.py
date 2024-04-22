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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс, который содержит общие атрибуты."""

    def __init__(self, body_color, position):
        self.body_color = body_color
        self.position = position

    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self, body_color, position):
        super().__init__(body_color, position)
        self.position = self.randomize_position()

    def randomize_position(self):
        x = randint(0, GRID_WIDTH) * GRID_SIZE
        y = randint(0, GRID_HEIGHT) * GRID_SIZE
        return (x, y)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, body_color, position):
        super().__init__(body_color, position)
        self.lenght = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
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
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self):
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

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.lenght = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
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


def main():
    # Инициализация PyGame:
    pygame.init()
    apple = Apple(APPLE_COLOR, (0, 0))
    apple.draw()
    center_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    snake = Snake(SNAKE_COLOR, center_position)
    snake.draw()
    pygame.display.update()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()

        # Если змея съела яблоко.
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.position = apple.randomize_position()

        # Если змея ударилась об себя.
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()
