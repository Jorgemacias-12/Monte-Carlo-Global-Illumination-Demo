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
    
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"{Fore.RED}Shader compile error: {error}{Style.RESET_ALL}")
    
    return shader