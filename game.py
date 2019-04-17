import random

import pygame
from pygame import Rect

from cell import Cell, CapturedMatrix


surface = pygame.display.set_mode((700, 700))
surface.fill((255, 255, 255))


MAX_X = 20
MAX_Y = 20

matrix = []
y = 10
for i in range(MAX_Y):
    x = 10
    row = []
    for j in range(MAX_X):
        row.append(Cell(surface, 0, Rect(x, y, 25, 25), (i, j)))
        x += 30
    matrix.append(row)
    y += 30

# matrix[0][0].player_id = 1
# matrix[-1][-1].player_id = 2
# matrix[0][0].fill()
# matrix[-1][-1].fill()

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

for row in matrix:
    for cell in row:
        cell.draw()
pygame.display.update()


def change_player(player):
    if player < 3:
        return player + 1
    return 1


current_player = 1
CAPTURING = False
SOMETHING_WAS_CAPTURED = False
limit_1 = random.randrange(1, 7)
limit_2 = random.randrange(1, 7)

RUNNING = True
while RUNNING:
    if current_player == 1:
        pygame.draw.rect(surface, (255, 0, 0), Rect(10, 650, 25, 25), 0)
    elif current_player == 2:
        pygame.draw.rect(surface, (0, 0, 255), Rect(10, 650, 25, 25), 0)
    elif current_player == 3:
        pygame.draw.rect(surface, (0, 255, 0), Rect(10, 650, 25, 25), 0)
    elif current_player == 4:
        pygame.draw.rect(surface, (0, 0, 0), Rect(10, 650, 25, 25), 0)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            current_player = change_player(current_player)
            limit_1 = random.randrange(1, 7)
            limit_2 = random.randrange(1, 7)
            continue
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            results = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
            for row in matrix:
                for cell in row:
                    results[cell.player_id] += 1
            print(results)
            RUNNING = False
            break
        if event.type == pygame.QUIT:
            exit()
        print(limit_1, limit_2)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            captured_matrix = CapturedMatrix(limit_1, limit_2)
            pos = pygame.mouse.get_pos()
            for row in matrix:
                for cell in row:
                    if cell.rect.collidepoint(pos) and cell.player_id == 0 and cell.can_be_capture(matrix,
                                                                                                   current_player):
                        print('DOWN')
                        captured_matrix.start(cell)
                        CAPTURING = True
                        break

        if event.type == pygame.MOUSEMOTION and CAPTURING:
            pos = pygame.mouse.get_pos()
            for row in matrix:
                for cell in row:
                    if cell.rect.collidepoint(pos) and cell.player_id == 0:
                        # cell.capture(current_player)
                        captured_matrix.update(cell)
                        # print(cell.position)

        if event.type == pygame.MOUSEBUTTONUP:
            if captured_matrix.any() and captured_matrix.is_available(matrix):
                for row in captured_matrix.normalize(matrix):
                    for cell in row:
                        if cell:
                            cell.capture(current_player)
                current_player = change_player(current_player)
                limit_1 = random.randrange(1, 7)
                limit_2 = random.randrange(1, 7)
            CAPTURING = False

    pygame.display.update()

pygame.exit()

