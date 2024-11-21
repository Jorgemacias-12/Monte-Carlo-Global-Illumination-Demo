import pygame
import numpy
import os

from pygame.locals import DOUBLEBUF, OPENGL
from pygame.time import Clock
from OpenGL.GL import *
from OpenGL.GLU import *

from .Shapes import Shapes
from .Utils import compile_shader, drawText, load_shader_from_file
from math import cos, sin, radians
from colorama import init, Fore, Style


class Application():
    screen_w = 1920
    screen_h = 1080

    resolution = (screen_w, screen_h)

    bg = (0, 0, 0, 1)
    drawing_color = (1, 1, 1, 1)

    screen = None
    clock = None

    done = False
    framerate = 60
    draw_manager = Shapes()

    pbo = None

    camera_pos = [0, 0, 0]
    camera_front = [0, 0, -1]
    camera_up = [0, 1, 0]
    camera_speed = 0.1
    yaw = 0
    pitch = 0
    mouse_sensitivity = 0.2

    framebuffer = None

    vertex = None
    fragment = None

    program = None

    def __init__(self):
        pygame.init()
        init()
        
        # Init all pygame resources
        self.screen = pygame.display.set_mode(
            self.resolution,
            pygame.FULLSCREEN | DOUBLEBUF | OPENGL
        )

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.clock = Clock()

        if glGenFramebuffers:
            self.pbo = glGenFramebuffers(1)

        self.vertex = load_shader_from_file(
            os.path.join("assets", "shaders", "vertex.glsl"))
        self.fragment = load_shader_from_file(
            os.path.join("assets", "shaders", "fragment.glsl"))

        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, self.pbo)
        glBufferData(GL_PIXEL_UNPACK_BUFFER, self.screen_w *
                     self.screen_h * 3, None, GL_STREAM_DRAW)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_COLOR_MATERIAL)

        glViewport(0, 0, self.screen_w, self.screen_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.screen_w / self.screen_h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        pygame.display.set_caption(
            "JAMZ - Monte Carlo Global Illumination - Demo")

        if not glGetString(GL_VERSION):
            print("Error: No OpenGL context.")
            self.done = True

        self.program = self.create_shader_program()
        
    def create_shader_program(self):
        vertex_shader = compile_shader(self.vertex, GL_VERTEX_SHADER)
        fragment_shader = compile_shader(self.fragment, GL_FRAGMENT_SHADER)

        program = glCreateProgram()

        if not program:
            raise RuntimeError(f"{Fore.RED}Failed to create shader program.{Style.RESET_ALL}")
    
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(program).decode()
            raise RuntimeError(f"{Fore.RED}Program link error: {
                               error}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Shader program linked successfully!{Style.RESET_ALL}")        
        
        return program

    def update_camera(self):
        glLoadIdentity()
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],
                  self.camera_pos[0] + self.camera_front[0],
                  self.camera_pos[1] + self.camera_front[1],
                  self.camera_pos[2] + self.camera_front[2],
                  self.camera_up[0], self.camera_up[1], self.camera_up[2])

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotate(1, 10, 0, 1)
        # glPushMatrix()
        # self.draw_manager.cube()
        # glPopMatrix()

        self.draw_manager.draw_scene()

        self.update_camera()

        drawText((10, 50, 0), f"Debug Info")
        drawText((10, 25, 0), f"Current position: {self.camera_pos}")
        drawText((10, 10, 0), f"FPS: {self.clock.get_fps():.0f}")

    def handle_mouse_motion(self, event):
        self.yaw += event.rel[0] * self.mouse_sensitivity
        self.pitch -= event.rel[1] * self.mouse_sensitivity

        self.pitch = max(-89, min(89, self.pitch))

        direction = [
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ]

        magnitude = (sum(d ** 2 for d in direction)) ** 0.5
        self.camera_front = [d / magnitude for d in direction]

    def run(self):
        while not self.done:
            self.clock.tick(self.framerate) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                self.done = True

            if keys[pygame.K_w]:
                self.camera_pos[0] += self.camera_front[0] * self.camera_speed
                self.camera_pos[1] += self.camera_front[1] * self.camera_speed
                self.camera_pos[2] += self.camera_front[2] * self.camera_speed
            if keys[pygame.K_s]:
                self.camera_pos[0] -= self.camera_front[0] * self.camera_speed
                self.camera_pos[1] -= self.camera_front[1] * self.camera_speed
                self.camera_pos[2] -= self.camera_front[2] * self.camera_speed
            if keys[pygame.K_a]:
                right = numpy.cross(self.camera_front, self.camera_up)
                self.camera_pos[0] -= right[0] * self.camera_speed
                self.camera_pos[2] -= right[2] * self.camera_speed
            if keys[pygame.K_d]:
                right = numpy.cross(self.camera_front, self.camera_up)
                self.camera_pos[0] += right[0] * self.camera_speed
                self.camera_pos[2] += right[2] * self.camera_speed

            self.display()
            pygame.display.flip()

        pygame.quit()
