import os
import pygame
import glm
from OpenGL.GL import *

from src.Utils import check_program_link_status, check_shader_compile_status, load_shader_from_file


class Application:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True

        # Init pygame and OpenGl
        pygame.init()
        pygame.display.set_mode(
            (self.width, self.height),
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL
        )
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
        vertices = [
            -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
            0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
            0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
        ]

        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(vertices))
                     (*vertices), GL_STATIC_DRAW)

        # Position attributes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Attributes of the normals
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                              6 * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.program)

        # Send the matrix
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE,
                           glm.value_ptr(self.model_matrix))
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE,
                           glm.value_ptr(self.view_matrix))
        glUniformMatrix4fv(
            self.projection_loc, 1, GL_FALSE, glm.value_ptr(
                self.projection_matrix)
        )

        # Send the light and the color
        glUniform3fv(self.light_pos_loc, 1, glm.value_ptr(self.light_pos))
        glUniform3fv(self.light_color_loc, 1, glm.value_ptr(self.light_color))
        glUniform3fv(self.object_color_loc, 1, glm.value_ptr(self.object_color))

        # Draw object
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.render()
            pygame.display.flip()

        pygame.quit()
