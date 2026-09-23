from src.config import *
from src.map import *
import colorama

colorama.just_fix_windows_console()

def main():
    dungeon = Dungeon(MAP_WIDTH, MAP_HEIGHT)
    dungeon.print_map()


if __name__ == "__main__":
    main()
