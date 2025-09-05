import pygame as pg
import numpy as np
class Configure:
    def __init__(   self,
                    width=800,
                    height=600,
                    title="Pygame Window",
                    icon=None
                ):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width, self.height))
        self.title = title
        self.icon = icon
    def get_screen(self):
        return self.screen

class Escene:
    def __init__(self,configure = Configure()):
        self.configure = configure
        self.frame = pg.surfarray.make_surface(np.zeros((self.configure.height, self.configure.width, 3), dtype=np.uint8))
    def run(self):
        pg.init()
        pg.display.set_caption(self.configure.title)
        if self.configure.icon:
            icon = pg.image.load(self.configure.icon)
            pg.display.set_icon(icon)
        
        running = True
        self.screen = self.configure.get_screen()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                self.handle_event(event)

            pg.time.delay(100)  # Pequeno atraso para reduzir o uso da CPU
            self.configure.screen.fill((0, 0, 0))
            self.configure.screen.blit(self.frame, (0, 0))  # Desenha o frame
            pg.display.flip()



    def set_frame(self,frame):
        self.frame = frame

    def handle_event(self, event):
        """Handle events in the scene"""
        pass