import pygame
import random
import math
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
    BAR_GRADIENTS = [
        (245, 183, 177),
        (230, 176, 170),
        (241, 148, 138)
    ]

    # FONTS
    FONT = pygame.font.SysFont("comicsans", 20)
    LARGE_FONT = pygame.font.SysFont("comicsans", 30)

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
        self.bar_height = math.floor((self.height -  self.TOP_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PADDING

def generate_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]


def draw(draw_info, sorting_algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # render title
    title = draw_info.LARGE_FONT.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()//2, 5))

    # render control text
    control_text = draw_info.FONT.render("R - Reset | SPACE - Start sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(control_text, (draw_info.width/2 - control_text.get_width()//2, 45))

    # sorting algorithms text
    sorting_algos_text = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting_algos_text, (draw_info.width/2 - sorting_algos_text.get_width()//2, 65))
    
    
    draw_bars(draw_info)
    pygame.display.update()


def draw_bars(draw_info, color_positions={}, clear_bg=False):

    if clear_bg:
        clear_rectangle = (draw_info.SIDE_PADDING, draw_info.TOP_PADDING, draw_info.width - 2 * draw_info.SIDE_PADDING, 
                           draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rectangle)

    for i, val in enumerate(draw_info.lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height

        color = draw_info.BAR_GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()


# sorting algorithms

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    for i in range(n - 1):
        for j in range(n-i-1):
            if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_bars(draw_info, {j: draw_info.RED, j+1: draw_info.GREEN}, clear_bg=True)
                yield True
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    for i in range(1, n):
        key = lst[i]
        j = i - 1
        while j >= 0 and ((lst[j] > key and ascending) or (lst[j] < key and not ascending)):
            lst[j+1] = lst[j]
            draw_bars(draw_info, {j: draw_info.RED, j+1: draw_info.GREEN}, clear_bg=True)
            yield True
            j -= 1
        lst[j+1] = key
    return lst


def main():
    run = True
    clock = pygame.time.Clock()
    sorting = False
    ascending = True

    n = 50
    min_val = 1
    max_val = 100
    lst = generate_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.set_lst(lst)

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info, ascending)
            
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_b and not sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"
            
            elif event.key == pygame.K_i and not sorting:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"


    pygame.quit()

if __name__ == "__main__":
    main() 
