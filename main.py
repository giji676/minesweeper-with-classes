from other_stuff.constants import WIDTH, HEIGHT, RESOLUTION, FPS, LIGHT_GRAY, TOTAL_MINES, BLACK, DARK_GRAY, WHITE, RED
from other_stuff.Button import Button
from other_stuff.Cell import Cell
import random
import pygame
import time

cell = Cell()

WIN = pygame.display.set_mode((WIDTH, HEIGHT + 200))
WIN.fill(LIGHT_GRAY)
pygame.font.init()

cols = int(WIDTH / RESOLUTION)
rows = int(HEIGHT / RESOLUTION)

myFont = pygame.font.SysFont('Arial', 40)

button1 = Button("Click here", x=250, y=520, bg="navy")

def show_button1():
    WIN.blit(button1.surface, (button1.x, button1.y))

def button1_click(event):
    x, y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            if button1.rect.collidedict(x, y):
                button1.change_text("Clicked", bg="red")


def make_2d_array():
    arr = []
    for i in range(cols):
        arr.append([])
        for j in range(rows):
            arr[i].append(Cell())

    return arr


def make_mines(grid):
    mine = 0
    while mine < TOTAL_MINES:
        rx = random.randint(0, cols-1)
        ry = random.randint(0, rows-1)

        if not grid[rx][ry].bomb:
            grid[rx][ry].bomb = True
            mine += 1
    return grid


def draw(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x = i * RESOLUTION
            y = j * RESOLUTION
            if grid[i][j].bomb:
                pygame.draw.rect(WIN, DARK_GRAY, (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

            if not grid[i][j].revealed and not grid[i][j].bomb:
                pygame.draw.rect(WIN, DARK_GRAY, (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

            if grid[i][j].revealed and not grid[i][j].bomb:
                pygame.draw.rect(WIN, WHITE, (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

            if grid[i][j].flagged:
                pygame.draw.rect(WIN, RED, (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

            if grid[i][j].neighbour_mines != 0:
                myFontRender = myFont.render(str(grid[i][j].neighbour_mines), True, RED)
                myFontSize = myFontRender.get_rect()
                myFontSize.center = (x + RESOLUTION / 2), (y + RESOLUTION / 2)
                WIN.blit(myFontRender, myFontSize)
                pygame.display.update()


def count_mines(grid, x, y):
    mines = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            newX = x + i
            newY = y + j
            if -1 < newX < cols and -1 < newY < rows:
                if grid[newX][newY].bomb:
                    mines += 1
    return mines


def print_grid(grid, dot):
    if dot == "b":
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                print(grid[x][y].bomb, end="")
            print()
    if dot == "r":
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                print(grid[x][y].revealed, end="")
            print()
    if dot == "m":
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                print(grid[x][y].neighbour_mines, end="  ")
            print()
    print(dot)


def search(grid, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            newX = x + i
            newY = y + j
            if -1 < newX < cols and -1 < newY < rows:
                if not grid[newX][newY].bomb and not grid[newX][newY].revealed and not grid[newX][newY].flagged:
                    mines = count_mines(grid, newX, newY)
                    if mines > 0:
                        grid[newX][newY].neighbour_mines = mines
                        grid[newX][newY].revealed = True
                    else:
                        grid[newX][newY].neighbour_mines = mines
                        grid[newX][newY].revealed = True
                        search(grid, newX, newY)
    return grid


def inputs(grid, mouse_events):
    pos = pygame.mouse.get_pos()
    if pos[1] > HEIGHT:
        return grid
    x = pos[0]//RESOLUTION
    y = pos[1]//RESOLUTION

    if mouse_events[0]:
        if grid[x][y].bomb:
            print("EXPLODED")
            time.sleep(3)
            main()
            return

        elif not grid[x][y].revealed:
            mines = count_mines(grid, x, y)
            grid[x][y].neighbour_mines = mines
            grid[x][y].revealed = True
            grid[x][y].flagged = False
            if mines == 0:
                grid = search(grid, x, y)

    if mouse_events[2]:
        grid[x][y].flagged = True
        grid[x][y].revealed = False
    return grid


def check_for_win(grid):
    bomb_count = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y].bomb and grid[x][y].flagged:
                bomb_count += 1
    if bomb_count == TOTAL_MINES:
        print("YOU WON!")
        #time.sleep(3)
        main()
        return


def main():
    run = True
    clock = pygame.time.Clock()

    grid = make_2d_array()
    grid = make_mines(grid)

    while run:
        clock.tick(FPS)

        mouse_events = pygame.mouse.get_pressed()

        if mouse_events[0] or mouse_events[2]:
            grid = inputs(grid, mouse_events)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                button1_click(event)
        show_button1()
        draw(grid)
        check_for_win(grid)

        pygame.display.update()
    pygame.quit()


main()
