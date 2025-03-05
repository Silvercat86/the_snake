import random
from sys import exit

import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (255, 255, 0)
DEFAULT_WHITE_COLOR = (255, 255, 255)

# Скорость змейки
SPEED = 10

# Различные позиции
DEFAULT_POSITION = (0, 0)
SNAKE_DEFAULT_POSITION = (20, 20)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self,
                 position=DEFAULT_POSITION,
                 body_color=DEFAULT_WHITE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объекта."""
        raise NotImplementedError(f"""Класс {self.__class__.__name__} 
                                  должен реализовать метод draw()""")

    def draw_rect(self, position):
        """Метод для отрисовки отдельного сегмента"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, color=APPLE_COLOR, impossible_positions=()):
        self.randomize_position(impossible_positions)
        super().__init__(self.position, color)

    def randomize_position(self, impossible_positions=()):
        """Определение позиции яблока."""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in impossible_positions:
                break

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, position=SNAKE_DEFAULT_POSITION, color=SNAKE_COLOR):
        super().__init__(position, color)
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку в выбранном направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        self.grow = False

    def draw(self):
        """Отрисовывает змейку."""
        for pos in self.positions:
            self.draw_rect(pos)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def get_all_positions(self):
        """Возвращает позицию всех частей змейки."""
        return self.positions

    def get_body_positions(self):
        """Возвращает позицию всех чатей кроме головы."""
        return self.positions[1:]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow = False


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция."""
    snake = Snake()
    apple = Apple(impossible_positions=snake.get_all_positions())

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.get_body_positions():
            snake.reset()

        if snake.get_head_position() == apple.position:
            snake.grow = True
            apple.randomize_position(snake.get_all_positions())

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
