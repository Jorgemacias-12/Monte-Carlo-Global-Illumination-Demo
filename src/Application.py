import pygame

from pygame.locals import DOUBLEBUF, OPENGL
from pygame.time import Clock
from OpenGL.GL import *
from OpenGL.GLU import *


class Application():
    screen_w = 800
    screen_h = 600

    resolution = (screen_w, screen_h)

    bg = (0, 0, 0, 1)
    drawing_color = (1, 1, 1, 1)

    screen = None
    clock = None
    
    done = False
    
    framerate = 60

    def __init__(self):
        # Init pygame duh!
        pygame.init()

        # Init all pygame resources
        self.screen = pygame.display.set_mode(
            self.resolution,
            DOUBLEBUF | OPENGL
        )

        self.clock = Clock()

        # Apply Background and drawing color
        glClearColor(self.bg[0], self.drawing_color[1],
                     self.bg[2], self.drawing_color[3])
        glColor(self.drawing_color)

        # Camera system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # args = fov(y), aspect ratio, zNear, zFar
        gluPerspective(60, (self.screen_w / self.screen_h), 0.1, 100.0)

        # Model View
        glMatrixMode(GL_MODELVIEW)
        glTranslate(0, 0, -5)
        glLoadIdentity()
        glViewport(0, 0, self.screen.get_width(), self.screen.get_height())
        glEnable(GL_DEPTH_TEST)
        glTranslate(0, 0, -2)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotate(1, 10, 0, 1)
        glPushMatrix()
        # TODO: import and execute here cube
        glPopMatrix()

    def run(self):
        while not self.done:
            self.clock.tick(self.framerate) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.display()
            
            pygame.display.flip()
            pygame.display.set_caption(f"JAMZ - Montecarlo demo - {self.clock.get_fps():.0f} fps")
            
        pygame.quit()