import os
import math
import pygame

from OpenGL.GL import *

from colorama import Fore, Style


def drawText(position, text):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    font = pygame.font.Font(None, 20)
    textSurface = font.render(text, True, (255, 255, 66))

    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    textData = pygame.image.tostring(textSurface, "RGBA", True)
    width, height = textSurface.get_size()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)

    enableOrtho(width, height)

    glPushMatrix()
    glTranslatef(position[0], position[1], 0.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(width, 0)
    glTexCoord2f(1, 1)
    glVertex2f(width, height)
    glTexCoord2f(0, 1)
    glVertex2f(0, height)
    glEnd()

    glPopMatrix()

    disableOrtho()

    glDeleteTextures(1, [texture])
    glDisable(GL_BLEND)


def enableOrtho(width, height):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)


def disableOrtho():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def load_shader_from_file(path):
    with open(path, 'r') as file:
        return file.read()


def check_shader_compile_status(shader, name):
    status = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if status != GL_TRUE:
        log = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"{Fore.RED}{name} compilation error: {log}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}GLSL Program compiled successfully!{Style.RESET_ALL}")



def check_program_link_status(program):
    status = glGetProgramiv(program, GL_LINK_STATUS)
    if not status:
        log = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Program linking error: {log}")


def select_resolution():
    pygame.init()

    resolutions = pygame.display.list_modes()

    print(f"{Fore.CYAN}Select a resolution:{Style.RESET_ALL}")
    for idx, resolution in enumerate(resolutions, 1):
        print(f"{Fore.GREEN}{idx}. {resolution[0]}x{resolution[1]}{Style.RESET_ALL}")

    try:
        selection = int(input(
            f"{Fore.CYAN}Give the number of the desired resolution: {Style.RESET_ALL}"))
        if 1 <= selection <= len(resolutions):
            selected_resolution = resolutions[selection - 1]
            return selected_resolution[0], selected_resolution[1]
        else:
            print(f"{Fore.RED}Invalid selection. a default value would be used instead.{Style.RESET_ALL}")
            return 800, 600  # Valor por defecto
    except ValueError:
        print(f"{Fore.RED}Please, give a valid number. a default value would be used.{Style.RESET_ALL}")
        return 800, 600


def get_max_resolution():
    pygame.init()
    resolutions = pygame.display.list_modes()

    max_resolution = max(resolutions, key=lambda res: res[0] * res[1])
    return max_resolution[0], max_resolution[1]


def generate_sphere(radius, sectors, stacks):
    vertices = []

    for stack in range(stacks + 1):
        stack_angle = math.radians(90 - stack * 180 / stacks)
        xy = radius * math.cos(stack_angle)
        z = radius * math.sin(stack_angle)

        for sector in range(sectors + 1):
            sector_angle = math.radians(sector * 360 / sectors)
            x = xy * math.cos(sector_angle)
            y = xy * math.sin(sector_angle)
            
            length = math.sqrt(x * x + y * y + z * z)
            nx, ny, nz = x / length, y / length, z / length
            
            vertices.extend([x, y, z, nx, ny, nz])
    
    return vertices

def drawText(position, text, program):
    glUseProgram(0)
    
    font_path = os.path.join("assets", "fonts", "Monocraft.ttf")

    font = pygame.font.Font(font_path, 20)
    
    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    
    glWindowPos3d(*position)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)
    
    glDisable(GL_BLEND)
    
    glUseProgram(program)
    