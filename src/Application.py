from math import cos, radians, sin
import os
import pygame
import numpy
import glm
from OpenGL.GL import *

from src.Utils import check_program_link_status, check_shader_compile_status, disableOrtho, drawText, enableOrtho, generate_sphere, load_shader_from_file


class Application:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True
        self.clock = pygame.time.Clock()

        # Init pygame and OpenGl
        pygame.init()
        pygame.display.set_mode(
            (self.width, self.height),
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL
        )
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(
            F"JAMZ - Monte Carlo Global Illumination Demo")
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        # Shader compilation
        self.program = self.create_shader_program()
        glUseProgram(self.program)

        # Get unfiform locations
        self.model_loc = glGetUniformLocation(self.program, "model")
        self.view_loc = glGetUniformLocation(self.program, "view")
        self.projection_loc = glGetUniformLocation(self.program, "projection")
        self.light_pos_loc = glGetUniformLocation(self.program, "lightPos")
        self.light_color_loc = glGetUniformLocation(self.program, "lightColor")
        self.object_color_loc = glGetUniformLocation(
            self.program, "objectColor")

        # Matrix configuration
        self.model_matrix = glm.mat4(1.0)
        self.view_matrix = glm.lookAt(
            glm.vec3(0.0, 0.0, 3.0), glm.vec3(
                0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0)
        )
        self.projection_matrix = glm.perspective(
            glm.radians(45.0), width / height, 0.1, 100.0
        )

        # Light configuration
        self.light_pos = glm.vec3(1.2, 1.0, 2.0)
        self.light_color = glm.vec3(1.0, 1.0, 1.0)
        self.object_color = glm.vec3(1.0, 0.5, 0.31)

        # Camera settings
        self.camera_pos = glm.vec3(0.0, 0.0, 3.0)
        self.camera_front = glm.vec3(0.0, 0.0, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)
        self.camera_speed = 0.05
        self.mouse_sensitivity = 0.1

        self.yaw = -90.0
        self.pitch = 0.0

        self.setup_object()

    def create_shader_program(self):
        vertex = load_shader_from_file(
            os.path.join("assets", "shaders", "vertex.glsl"))
        fragment = load_shader_from_file(
            os.path.join("assets", "shaders", "fragment.glsl"))

        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vertex)
        glCompileShader(vs)
        check_shader_compile_status(vs, "Vertex Shader")

        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, fragment)
        glCompileShader(fs)
        check_shader_compile_status(fs, "Fragment Shader")

        program = glCreateProgram()
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        glLinkProgram(program)
        check_program_link_status(program)

        glDeleteShader(vs)
        glDeleteShader(fs)

        return program

    def setup_object(self):
        cube_vertices = [
            # Position          # Normal
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0, # Face 1
            0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,

            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
            -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,

            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0, # Face 2
            0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,

            -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,
            0.5,  0.5,  0.5,  0.0,  0.0,  1.0,
            -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,

            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0, # Face 3
            -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,

            -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
            -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,

            0.5,  0.5,  0.5,  1.0,  0.0,  0.0, # Face 4
            0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,

            0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
            0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
            0.5, -0.5,  0.5,  1.0,  0.0,  0.0,

            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0, # Face 5
            0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,

            -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
            0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
            -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,

            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0, # Face 6
            0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,

            -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
            0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
            -0.5,  0.5,  0.5,  0.0,  1.0,  0.0
        ]


        self.cube_vao = glGenVertexArrays(1)
        self.cube_vbo = glGenBuffers(1)

        glBindVertexArray(self.cube_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.cube_vbo)
        glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(cube_vertices))
                     (*cube_vertices), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.sphere_vertices = generate_sphere(1.0, 36, 18)

        self.sphere_vao = glGenVertexArrays(1)
        self.sphere_vbo = glGenBuffers(1)

        glBindVertexArray(self.sphere_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.sphere_vbo)
        glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(self.sphere_vertices))
                     (*self.sphere_vertices), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.program)

        # Projection matrices setup
        glUniformMatrix4fv(self.view_loc, 
                           1, 
                           GL_FALSE,
                           glm.value_ptr(self.view_matrix))
        glUniformMatrix4fv(
            self.projection_loc,
            1, 
            GL_FALSE, 
            glm.value_ptr(self.projection_matrix)
        )

        # Render cube 
        self.model_matrix = glm.mat4(1.0)
        self.model_matrix = glm.translate(
            self.model_matrix,
            glm.vec3(0.0, 0.0, 5.0)
        )
        glUniformMatrix4fv(
            self.model_loc,
            1,
            GL_FALSE,
            glm.value_ptr(self.model_matrix)
        )        

        glUniform3fv(self.light_color_loc,
                     1,
                     glm.value_ptr(self.light_color))
        
        glUniform3fv(self.object_color_loc,
                     1,
                     glm.value_ptr(self.object_color))
        
        glBindVertexArray(self.cube_vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
        
        
        # Render "Sun"
        self.model_matrix = glm.mat4(1.0)
        self.model_matrix = glm.translate(
            self.model_matrix,
            glm.vec3(1.2, 1.0, -2.0)
        )        
        glUniformMatrix4fv(
            self.model_loc,
            1,
            GL_FALSE,
            glm.value_ptr(self.model_matrix)
        )
        
        yellow_color = glm.vec3(1.0, 1.0, 0.0)
        
        glUniform3fv(self.light_color_loc, 1, glm.value_ptr(yellow_color))
        glUniform3fv(self.object_color_loc, 1, glm.value_ptr(yellow_color))
        
        glBindVertexArray(self.sphere_vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.sphere_vertices) // 3)
        glBindVertexArray(0)
        
        # TODO: refactor this in order to get it work!
        # enableOrtho(self.width, self.height)
        # drawText((10, 10), "Hello, OpenGL!")
        # disableOrtho()

    def update_camera(self):
        front = glm.vec3(
            glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.pitch)),
            glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        )
        self.camera_front = glm.normalize(front)

        self.view_matrix = glm.lookAt(
            self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def handle_mouse_motion(self, event):
        self.yaw += event.rel[0] * self.mouse_sensitivity
        self.pitch -= event.rel[1] * self.mouse_sensitivity
        self.pitch = glm.clamp(self.pitch, -89.0, 89.0)
        self.update_camera()

    def handle_keyboard_input(self, keys):
        if keys[pygame.K_ESCAPE]:
            self.running = False

        if keys[pygame.K_w]:
            self.camera_pos += self.camera_front * self.camera_speed
        if keys[pygame.K_s]:
            self.camera_pos -= self.camera_front * self.camera_speed
        if keys[pygame.K_a]:
            right = glm.cross(self.camera_front, self.camera_up)
            self.camera_pos -= glm.normalize(right) * self.camera_speed
        if keys[pygame.K_d]:
            right = glm.cross(self.camera_front, self.camera_up)
            self.camera_pos += glm.normalize(right) * self.camera_speed

        self.update_camera()

    def run(self):
        while self.running:
            # TODO: make this a config flag in __main__.py
            self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)

            self.handle_keyboard_input(pygame.key.get_pressed())
            self.render()
            pygame.display.flip()

        pygame.quit()
