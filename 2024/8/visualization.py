from colorama import Fore, Style, init

init(autoreset=True)

# TODO:  Need to propery link antennas to their correspodning antinodes some bug right now.  Debug later.
def print_grid(grid, antennas, antinodes):
    colors = [
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
        Fore.LIGHTRED_EX,
        Fore.LIGHTGREEN_EX,
        Fore.LIGHTYELLOW_EX,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX,
        Fore.LIGHTWHITE_EX,
    ]
    
    freq_to_color = {}
    for i, freq in enumerate(antennas.keys()):
        freq_to_color[freq] = colors[i % len(colors)]
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            is_antenna, is_antinode = False, False
            color = Style.RESET_ALL
            
            for freq, coords in antennas.items():
                if (x, y) in coords:
                    color = freq_to_color[freq]
                    print(f"{color}{freq}{Style.RESET_ALL}", end='')
                    is_antenna = True
                    break
            
            if (x, y) in antinodes:
                if not is_antenna:
                    color = Style.RESET_ALL
                print(f"{color}#{Style.RESET_ALL}", end='')
                is_antinode = True
            
            if not is_antenna and not is_antinode:
                print('.', end='')
        
        print()

