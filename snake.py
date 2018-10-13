import numpy as np
import random

class Vector:

    def __init__(self, x, y = 0):
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        elif isinstance(other, tuple):
            return Vector(self.x * other[0], self.y * other[1])
        else:
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        elif isinstance(other, tuple):
            return Vector(self.x / other[0], self.y / other[1])
        else:
            return Vector(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x // other.x, self.y // other.y)
        elif isinstance(other, tuple):
            return Vector(self.x // other[0], self.y // other[1])
        else:
            return Vector(self.x // other, self.y // other)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        else:
            return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + " , " + str(self.y) + ")"

    def left(self):
        if self == Vector.UP:
            return Vector(Vector.LEFT)
        elif self == Vector.LEFT:
            return Vector(Vector.DOWN)
        elif self == Vector.DOWN:
            return Vector(Vector.RIGHT)
        else:
            return Vector(Vector.UP)

    def right(self):
        if self == Vector.UP:
            return Vector(Vector.RIGHT)
        elif self == Vector.LEFT:
            return Vector(Vector.UP)
        elif self == Vector.DOWN:
            return Vector(Vector.LEFT)
        else:
            return Vector(Vector.DOWN)




SNAKE_VALUE = 0.5
APPLE_VALUE = 0.25
COMMAND_STRAIGHT = 0
COMMAND_LEFT = -1
COMMAND_RIGHT = 1

class Snake:
    def __init__(self, position, direction, length):
        self.position = position
        if isinstance(direction, tuple): #convert tuples (direction constants) to vectors
            direction = Vector(direction)
        self.direction = direction
        self.length = length
        self.tiles = []

class Game:
    def __init__(self, field_size, snake):
        self.field = np.zeros(field_size) #init field
        self.snake = snake
        self.score = 0
        self.running = True #keeps track if the snake is still alive
        self.steps = 0
        self.used_fields = []

        for i in range(self.snake.length):  # create snake
            new_position = self.snake.position + Vector(-i * self.snake.direction.x, -i * self.snake.direction.y)
            if self.valid_position(new_position):  # dont allow positions outside of the field
                self.field[new_position.x][new_position.y] = SNAKE_VALUE
                self.snake.tiles.append(new_position)

        self.add_apple()

    def update(self, command):
        if self.running:  # only update game if snake is still alive and the game running
            if command == COMMAND_LEFT:  # update snake direction
                self.snake.direction = self.snake.direction.right()
            elif command == COMMAND_RIGHT:
                self.snake.direction = self.snake.direction.left()

            next_position = self.snake.position + self.snake.direction  # get next position of snake
            if not self.valid_position(next_position):  # snake ran into walls
                self.running = False
            else:
                next_value = self.field[next_position.x][next_position.y]
                if (next_value >= SNAKE_VALUE):  # ran into snake body
                    self.running = False
                else:
                    self.field[next_position.x][next_position.y] = SNAKE_VALUE  # add new body part
                    self.snake.position = next_position
                    self.snake.tiles.insert(0, next_position)
                    self.steps += 1
                    pos_hash = next_position.y * self.field.shape[0] + next_position.x
                    if not pos_hash in self.used_fields:
                        self.used_fields.append(pos_hash)

                    if next_value != APPLE_VALUE:  # no apple remove last snake body part
                        last_position = self.snake.tiles[self.snake.length]
                        self.field[last_position.x][last_position.y] = 0  # remove last body part
                        del self.snake.tiles[self.snake.length]
                    else:  # hit apple, up score
                        self.score += 1
                        self.snake.length += 1
                        self.add_apple()

    # check if position is within the field
    def valid_position(self, position):
        return position.x >= 0 and position.x < self.field.shape[0] and position.y >= 0 and position.y < self.field.shape[1]

    # determine position of next apple
    def add_apple(self):
        position = Vector(random.randint(0, self.field.shape[0] - 1), random.randint(0, self.field.shape[1] - 1))
        while self.field[position.x][position.y] > 0:  # generate new position until empty spot is found
            position = Vector(random.randint(0, self.field.shape[0] - 1), random.randint(0, self.field.shape[1] - 1))
        self.field[position.x][position.y] = APPLE_VALUE

    # find the last body part of the snake
    def snake_end(self):
        current_direction = self.snake.direction
        current_position = self.snake.position
        for i in range(self.snake.length):
            next_position = current_position - current_direction
            if self.field[next_position.x][next_position.y] != SNAKE_VALUE: #snake turned, no body found
                next_position = current_position - current_direction.left() #try on the left
                if self.field[next_position.x][next_position.y] != SNAKE_VALUE: #not found on the left
                    next_position = current_direction - current_direction.right() #try on the right
                    if self.field[next_position.x][next_position.y] == SNAKE_VALUE:
                        current_direction = current_direction.right()
                else:
                    current_direction = current_direction.left()
            current_position = next_position
        return current_position
