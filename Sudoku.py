import random

current_puzzle = [[0, 0, 2, 0, 5, 8, 0, 0, 1],
                  [0, 8, 0, 2, 1, 0, 0, 0, 0],
                  [0, 4, 1, 3, 9, 0, 8, 0, 2],
                  [1, 5, 0, 0, 2, 9, 0, 3, 8],
                  [0, 2, 9, 8, 3, 5, 4, 1, 6],
                  [8, 3, 0, 1, 7, 0, 9, 2, 5],
                  [2, 0, 8, 0, 4, 3, 0, 6, 9],
                  [0, 0, 0, 0, 6, 2, 0, 8, 4],
                  [4, 0, 0, 9, 8, 1, 2, 0, 0]]


def gen_possible_combos(num):
    combos = []
    if num == 2:
        for i in range(1, 10):
            for x in range(1, 10):
                if i != x:
                    combos.append([i, x])
    if num == 3:
        for x in range(1, 10):
            for y in range(1, 10):
                if y > x:
                    for z in range(1, 10):
                        if z > y:
                            combos.append([x, y, z])
    return combos



class Manager:

    def __init__(self):
        # 0 is an empty space
        self.puzzle = []
        self.set_up(current_puzzle, self.puzzle)
        self.blind_filled = []

    def __str__(self):
        string = ""
        for row in self.puzzle:
            for space in row:
                string += str(space) + ' '
            string += '\n'
        return string

    def set_up(self, puzzle, board):
        x = 0
        for row in puzzle:
            board.append([])
            y = 0
            for column in puzzle:
                board[x].append(Space(puzzle[x][y], x, y))
                y += 1
            x += 1

    def row(self, row):
        return self.puzzle[row]

    def column(self, column):
        array = []
        for row in self.puzzle:
            array.append(row[column])
        return array

    def block(self, block):
        array = []
        column = 0
        row = 0
        if block == 1:
            column = 3
        elif block == 2:
            column = 6
        elif block == 3:
            row = 3
        elif block == 4:
            row = 3
            column = 3
        elif block == 5:
            row = 3
            column = 6
        elif block == 6:
            row = 6
        elif block == 7:
            row = 6
            column = 3
        elif block == 8:
            row = 6
            column = 6

        for i in range(3):
            for x in range(3):
                array.append(self.puzzle[row][column])
                column += 1
            column -= 3
            row += 1
        return array

    def check_possible(self, list):
        numbers = []
        for space in list:
            if space.value > 0:
                numbers.append(space.value)
        for space in list:
            for number in numbers:
                if number in space.possible:
                    space.remove(number)
        for i in range(1, 10):
            if i not in numbers:
                possible = []
                for slot in list:
                    if i in slot.possible:
                        possible.append(slot)
                if len(possible) == 1:
                    possible[0].value = i

    def direct_place(self):
        for row in self.puzzle:
            for space in row:
                if space.value == 0:
                    if len(space.possible) == 1:
                        space.value = space.possible[0]
                        return True
                    print space.possible

    def check_doubles(self, list):
        for combo in possible_doubles:
            spaces = []
            for space in list:
                if combo[0] in space.possible or combo[1] in space.possible:
                    spaces.append(space)
            if len(spaces) == 2:
                for space in spaces:
                    for num in space.possible:
                        if num not in combo:
                            space.remove(num)

    def check_triples(self):
        pass



    # def bowmans_bingo(self):
    #     for row in self.puzzle:
    #         for space in row:
    #             if space.value == 0:
    #                 x = 0
    #                 space.value = space.possible[0]

    def solve(self):
        placed = True
        while placed:
            placed = False
            for i in range(9):
                self.check_possible(self.row(i))
                self.check_possible(self.column(i))
                self.check_possible(self.block(i))
            placed = self.direct_place()
            if not placed:
                print "doubles"
                for i in range(9):
                    self.check_doubles(self.row(i))
                    self.check_doubles(self.column(i))
                    self.check_doubles(self.block(i))
                placed = self.direct_place()


class Space:

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if self.value > 0:
            self.possible = []

    def __str__(self):
        return str(self.value)

    def remove(self, x):
        if type(x) is list:
            for i in x:
                if i in self.possible:
                    self.possible.remove(i)
        else:
            if x in self.possible:
                self.possible.remove(x)

possible_doubles = gen_possible_combos(2)
possible_triples = gen_possible_combos(3)
game = Manager()
game.solve()
print game
