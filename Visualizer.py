import pygame_matplotlib
import pygame
import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self):
        width, height = 900, 600
        self.fps = 60
    
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Maze Visualizer")

    def start_simul(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        
            self.draw_window()

        pygame.quit()


    def draw_window(self):
        self.window.fill((255,200,255))
        fig, axes = plt.subplots(1, 1,)
        axes.plot([1,2], [1,2], color='green', label='test')
        
        self.window.blit(fig, (100, 100))
        pygame.display.update()







