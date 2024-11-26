from src.Application import Application
from colorama import init, Fore, Style
import sys
from src.Utils import get_max_resolution, select_resolution

if __name__ == "__main__":
    init()

    if "--config-res" in sys.argv:
        width, height = select_resolution()
    else:
        width, height = get_max_resolution()
        
    app = Application(width, height)
    app.run()
    