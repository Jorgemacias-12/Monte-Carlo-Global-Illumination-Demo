import pygame
import platform

from pygame.locals import DOUBLEBUF, OPENGL
from pygame.time import Clock
from OpenGL.GL import *
from OpenGL.GLU import *
from .Shapes import Shapes
from .Utils import drawText

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

    draw_manager = Shapes()

    def __init__(self):
        # Init pygame duh!
        pygame.init()

        # Init all pygame resources
        self.screen = pygame.display.set_mode(
            self.resolution,
            DOUBLEBUF | OPENGL
        )

        self.clock = Clock()

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

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        pygame.display.set_caption(
            "JAMZ - Monte Carlo Global Illumination - Demo")

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotate(1, 10, 0, 1)
        glPushMatrix()
        self.draw_manager.cube()
        glPopMatrix()

        drawText((10, 25, 0), f"Debug Info")
        drawText((10, 10, 0), f"FPS: {self.clock.get_fps():.0f}")        

    def run(self):
        while not self.done:
            self.clock.tick(self.framerate) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.display()
            pygame.display.flip()
        
        pygame.quit()