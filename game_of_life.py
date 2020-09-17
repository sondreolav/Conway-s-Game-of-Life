"""
Conway's Game of Life.
Author: Sondre Nesje.
Licence: https://creativecommons.org/licenses/by-sa/4.0/
Year: 2020
"""

import sys
from random import randint

import pygame

#Screen settings
FPS = 10
SCREEN_WIDTH = SCREEN_HEIGHT = 600

#Cell settings
CELL_SIZE = 3
CELL_WIDTH = int(SCREEN_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(SCREEN_HEIGHT / CELL_SIZE)

#Grid size
GRID_WIDTH = int(SCREEN_WIDTH / CELL_SIZE)
GRID_HEIGHT = int(SCREEN_HEIGHT / CELL_SIZE)

#Chance to make a cell at the beginning.
#In percent (%)
CELL_CHANCE = 20

#Color settings
BACKGROUND_COLOR = (128, 0, 128)
CELL_COLOR = (255, 255, 0)

def main():
    """Main game function"""

    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game of life")

    cells = create_cells()

    run_game(screen, fps_clock, cells)

def run_game(screen, fps_clock, cells):
    """The main loop for the game"""

    while True:
        check_events()

        cells = update_cells(cells)

        update_screen(screen, fps_clock, cells)

def check_events():
    """Respond to events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def create_cells():
    """Create a set of alive cells"""

    cells = set()

    for column in range(CELL_WIDTH):
        for row in range(CELL_HEIGHT):

            #The cell's x and y coordinates
            cell_x = column * CELL_SIZE
            cell_y = row * CELL_SIZE
            cell = (cell_x, cell_y)

            if CELL_CHANCE > randint(0, 100):
                cells.add(cell)

    return cells

def update_cells(old_cells):
    """Update the state of the cells"""

    #One set for new cells for the next generation,
    #and one for dead neighbor cells
    new_cells = set()
    dead_neighbor_cells = set()

    for cells_alive in (True, False):

        #Go through both living cells and dead neighbor cells
        if cells_alive:
            cells = old_cells.copy()
        else:
            cells = dead_neighbor_cells.copy()

        for cell in cells:

            #A set of neighbor cells
            neighbor_cells = check_neighbor_cells(cell)

            #A variable for live neighbor cells
            live_cell_neighbors = 0

            #Count neighboring cells
            #and make a set of dead neighbor cells
            for neighbor_cell in neighbor_cells:
                if neighbor_cell in old_cells:
                    #Count how many neighboring cells are alive
                    live_cell_neighbors += 1
                elif cells_alive:
                    #Create a set of dead neighbor cells,
                    #but only if the main cell is alive
                    dead_neighbor_cells.add(neighbor_cell)

            #Cellular automaton rule
            if cells_alive and 2 <= live_cell_neighbors <= 3:
                #The cell survives
                new_cells.add(cell)
            elif not cells_alive and live_cell_neighbors == 3:
                #The cell comes alive
                new_cells.add(cell)
            #else:
            #    The cell dies, or remains dead

    return new_cells.copy()

def check_neighbor_cells(cell):
    """Function to check for neighbor cells"""

    #The cell's x and y coordinates
    cell_x = cell[0]
    cell_y = cell[1]

    #Make a set of neighbor cells
    neighbor_cells = {
        tuple((cell_x - 1 * CELL_SIZE, cell_y - 1 * CELL_SIZE)),
        tuple((cell_x + 0 * CELL_SIZE, cell_y - 1 * CELL_SIZE)),
        tuple((cell_x + 1 * CELL_SIZE, cell_y - 1 * CELL_SIZE)),
        tuple((cell_x - 1 * CELL_SIZE, cell_y + 0 * CELL_SIZE)),
        tuple((cell_x + 1 * CELL_SIZE, cell_y + 0 * CELL_SIZE)),
        tuple((cell_x - 1 * CELL_SIZE, cell_y + 1 * CELL_SIZE)),
        tuple((cell_x + 0 * CELL_SIZE, cell_y + 1 * CELL_SIZE)),
        tuple((cell_x + 1 * CELL_SIZE, cell_y + 1 * CELL_SIZE))}

    return neighbor_cells

def update_screen(screen, fps_clock, cells):
    """Update the screen, and flip to the new screen"""

    screen.fill(BACKGROUND_COLOR)

    #Draw each alive cells
    for cell in cells:
        living_cell = pygame.Rect(cell[0], cell[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, CELL_COLOR, living_cell)

    #Make the most recently drawn screen visible.
    pygame.display.flip()

    fps_clock.tick(FPS)

if __name__ == "__main__":
    #Run the game.
    main()