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


def select_resolution():
    pygame.init()

    resolutions = pygame.display.list_modes()

    print(f"{Fore.CYAN}Select a resolution:{Style.RESET_ALL}")
    for idx, resolution in enumerate(resolutions, 1):
        print(f"{Fore.GREEN}{idx}. {resolution[0]}x{
              resolution[1]}{Style.RESET_ALL}")

    try:
        selection = int(input(
            f"{Fore.CYAN}Give the number of the desired resolution: {Style.RESET_ALL}"))
        if 1 <= selection <= len(resolutions):
            selected_resolution = resolutions[selection - 1]
            return selected_resolution[0], selected_resolution[1]
        else:
            print(f"{Fore.RED}Invalid selection. a default value would be used instead.{
                  Style.RESET_ALL}")
            return 800, 600  # Valor por defecto
    except ValueError:
        print(f"{Fore.RED}Please, give a valid number. a default value would be used.{
              Style.RESET_ALL}")
        return 800, 600


def get_max_resolution():
    pygame.init()
    resolutions = pygame.display.list_modes()

    max_resolution = max(resolutions, key=lambda res: res[0] * res[1])
    return max_resolution[0], max_resolution[1]