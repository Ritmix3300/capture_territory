import pygame
from pygame import Rect

from colors import BLUE, RED, GREEN, BLACK


LIMIT_1 = 3
LIMIT_2 = 2


class Cell:
    def __init__(self, surface, player_id, rect, position):
        self.player_id = player_id
        self.rect = rect
        self.surface = surface
        self.position = position

    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 0), self.rect, 1)

    def fill(self):
        if self.player_id == 1:
            color = RED
        elif self.player_id == 2:
            color = BLUE
        elif self.player_id == 3:
            color = GREEN
        elif self.player_id == 4:
            color = BLACK

        pygame.draw.rect(self.surface, color, self.rect, 0)

    def capture(self, player_id):
        if self.player_id == 0:
            self.player_id = player_id
            self.fill()

    def can_be_capture(self, matrix, player_id):
        i, j = self.position
        if i == 0 and j == 0 and player_id == 1 or i == 0 and j == 19 and player_id == 2 or i == 19 and j == 10 and player_id == 3:# or i == 19 and j == 0 and player_id == 4:  # TODO UNHARDCODE
            return True
        try:
            if matrix[i][j-1].player_id == player_id:  # LEFT
                return True
        except IndexError:
            pass
        try:
            if matrix[i][j+1].player_id == player_id:  # RIGHT
                return True
        except IndexError:
            pass
        try:
            if matrix[i-1][j].player_id == player_id:  # UP
                return True
        except IndexError:
            pass
        try:
            if matrix[i+1][j].player_id == player_id:  # DOWN
                return True
        except IndexError:
            pass

        return False

    @property
    def x(self):
        return self.position[1]

    @property
    def y(self):
        return self.position[0]

    def __str__(self):
        return f'{self.y}:{self.x}'


class CapturedMatrix:
    def __init__(self, limit_1, limit_2):
        self.left = None
        self.top = None
        self.right = None
        self.bottom = None
        self.cells = []

        self.l1 = limit_1
        self.l2 = limit_2

        for i in range(20):  # TODO UNHARDCODE
            row = []
            for j in range(20):
                row.append(None)
            self.cells.append(row)

        self.horizontal_limit = LIMIT_1
        self.vertical_limit = LIMIT_2

    def start(self, cell: Cell):
        self.top, self.left = cell.position
        self.bottom, self.right = cell.position
        self.cells[cell.x][cell.y] = cell

    def update(self, cell: Cell):
        # if cell not in self.cells:
        y, x = cell.position
        if y != self.top or y != self.bottom and x != self.left or x!= self.right:
            # if (self.left + LIMIT_1-1 >= x and self.top + LIMIT_2-1 >= y or self.left + LIMIT_2-1 >= x and self.top + LIMIT_1-1 >= y or
            #     self.left - LIMIT_1+1 <= x and self.top - LIMIT_2+1 <=y or self.left - LIMIT_2+1 <= x and self.top - LIMIT_1+1 <=y):
            if (self.left + self.l1-1 >= x and self.top + self.l2-1 >= y or self.left + self.l2-1 >= x and self.top + self.l1-1 >= y or
                self.left - self.l1+1 <= x and self.top - self.l2+1 <=y or self.left - self.l2+1 <= x and self.top - self.l1+1 <=y):
                self.cells[cell.y][cell.x] = cell
                if cell.x > self.right:
                    self.right = cell.x
                if cell.y > self.bottom:
                    self.bottom = cell.y
                if cell.x < self.left:
                    self.left = cell.x
                if cell.y < self.top:
                    self.top = cell.y

    def is_available(self, matrix):
        temp_matrix = self.normalize(matrix)
        # if len(temp_matrix) == LIMIT_1 and len(temp_matrix[0]) == LIMIT_2 or len(temp_matrix) == LIMIT_2 and len(temp_matrix[0]) == LIMIT_1:
        if len(temp_matrix) == self.l1 and len(temp_matrix[0]) == self.l2 or len(temp_matrix) == self.l2 and len(temp_matrix[0]) == self.l1:
            return True
        return False

    def normalize(self, matrix):
        temp_matrix = []
        for i in range(self.top, self.bottom+1):
            row = []
            for j in range(self.left, self.right+1):
                row.append(matrix[i][j])
            temp_matrix.append(row)
        # for row in self.cells:
        #     if any(row):
        #         temp_matrix.append([cell for cell in row if cell])
        return temp_matrix

    def any(self):
        not_null = False
        for row in self.cells:
            not_null = any(row)
            if not_null:
                break
        return not_null
