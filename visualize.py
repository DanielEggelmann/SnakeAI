import pygame
import snake

class Visualizer:
    def __init__(self, resolution, title, tile_size, snake_color, apple_color):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        self.running = True
        pygame.display.set_caption(title)
        self.tile_size = tile_size
        self.snake_color = snake_color
        self.apple_color = apple_color
        self.key = None

    #must be called before drawing a frame
    def begin_frame(self):
        if self.running:
            self.key_a = False
            self.key_d = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return
                elif event.type == pygame.KEYDOWN and event.key == 100:
                    self.key = "A"
                elif event.type == pygame.KEYDOWN and event.key == 97:
                    self.key = "D"

            self.screen.fill((0, 0, 0))

    def draw_field(self, field, position):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(position[0], position[1], field.shape[0] * self.tile_size, field.shape[1] * self.tile_size)  ) #draw background
        for x in range(field.shape[0]):
            for y in range(field.shape[1]):
                type = field[x][y]
                if type == snake.SNAKE_VALUE:
                    pygame.draw.rect(self.screen, self.snake_color, pygame.Rect(position[0] + x * self.tile_size, position[1] + y * self.tile_size, self.tile_size, self.tile_size))
                elif type == snake.APPLE_VALUE:
                    pygame.draw.rect(self.screen, self.apple_color, pygame.Rect(position[0] + x * self.tile_size, position[1] + y * self.tile_size, self.tile_size, self.tile_size))

    #must be called after drawing
    def end_frame(self):
        if self.running:
            pygame.display.flip()

    def close(self):
        self.running = False
        pygame.quit()

    def get_ticks(self):
        return pygame.time.get_ticks()