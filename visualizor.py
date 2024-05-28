import pygame
import random
pygame.init()

class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GREY = (128, 128, 128)
    BACKGROUND_COLOR = WHITE
    SIDE_PADDING = 50
    TOP_PADDING = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
       
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_lst(lst)

    def set_lst(self, lst):
        self.lst = lst
        self.max_val = max(self.lst)
        self.min_val = min(self.lst)
        self.bar_width = round((self.width - 2 * self.SIDE_PADDING) / len(self.lst))
        # height of 1 unit of value
        self.bar_height = round((self.height -  self.TOP_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PADDING

def generate_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
    pygame.quit()

if __name__ == "__main__":
    main() 
