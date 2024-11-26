from src.Application import Application
from colorama import init, Fore, Style

if __name__ == "__main__":
    init()
    
    width = int(input(f"{Fore.CYAN}Desired width of the window: {Style.RESET_ALL}"))
    height = int(input(f"{Fore.CYAN}Desired height of the window: {Style.RESET_ALL}"))
    
    app = Application(width, height)
    app.run() 