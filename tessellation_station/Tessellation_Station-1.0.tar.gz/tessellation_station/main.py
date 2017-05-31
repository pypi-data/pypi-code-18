import sys
from tessellation_station import transformations
from tessellation_station.coordinate_grid import Grid
from os import path

IMAGE_SIZE = 1000
GRID_SIZE = 15
GRID = Grid(IMAGE_SIZE, GRID_SIZE)
C = transformations.C

def from_file():
    file_in = sys.argv[1]
    depth = int(sys.argv[2])
        
    with open(file_in) as file_in:
        commands = []
        for line in file_in:
            commands.append(line.rstrip())

    results = []
    i = 0
    while i < depth:
        for i, command in enumerate(commands):
            step = C.step(command)
            if step in ["config", "comment"]:
                # Filter out comments and configuration commands
                #commands.remove(i)
                continue

            if step in ["controlls"]:
                continue

            results.append(step)

        i += 1

    while True: # Repeat until a valid input
        print("Would you like to save to an image? y/n ")
        save = input("- ")
        if save in ["y", "Y"]:
            # Draw first polygon black
            GRID.draw_polygon(results[0], False)
            results.remove(results[0])
            for polygon in results:
                GRID.draw_polygon(polygon, True)

            file_name = path.splitext(file_in.name)[0]
            GRID.save(file_name)
            break

        if save in ["n", "N"]:
            print(results)
            break

def from_prompt():
    while True:
        print(C.step(input("- ")))

if __name__=="__main__":
    try:
        FILE_IN = sys.argv[1]
        DEPTH = int(sys.argv[2])

    except IndexError:
        from_prompt()

    from_file(FILE_IN, DEPTH)