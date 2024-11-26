import pygame

from OpenGL.GL import *

from colorama import Fore, Style


def drawText(position, text):
    font = pygame.font.Font(None, 20)
    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def load_shader_from_file(path):
    with open(path, 'r') as file:
        return file.read()


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)

    glShaderSource(shader, source)
    glCompileShader(shader)

    sucess = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not sucess:
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"{Fore.RED}Shader compile error: {
                           error}{Style.RESET_ALL}")

    return shader


def check_shader_compile_status(shader, name):
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not status:
        log = glGetShaderInfoLog(shader).decode()

        raise RuntimeError(f"{name} compilation error: {log}")


def check_program_link_status(program):
    status = glGetProgramiv(program, GL_LINK_STATUS)
    if not status:
        log = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Program linking error: {log}")
