import random

current_puzzle = [[0, 0, 0, 9, 2, 1, 0, 0, 3],
                  [0, 0, 9, 0, 0, 0, 0, 6, 0],
                  [0, 0, 0, 0, 0, 0, 5, 0, 0],
                  [0, 8, 0, 4, 0, 3, 0, 0, 6],
                  [0, 0, 7, 0, 0, 0, 8, 0, 0],
                  [5, 0, 0, 7, 0, 0, 0, 4, 0],
                  [0, 0, 3, 0, 0, 0, 0, 0, 0],
                  [0, 2, 0, 0, 0, 0, 7, 0, 0],
                  [8, 0, 0, 1, 9, 5, 0, 0, 0]]

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
            for cell in row:
                string += str(cell) + ' '
            string += '\n'
        return string

    def set_up(self, puzzle, board):
        x = 0
        for row in puzzle:
            board.append([])
            y = 0
            for column in puzzle:
                board[x].append(Cell(puzzle[x][y], x, y))
                y += 1
            x += 1
        for i in range(9):
            for cell in self.block(i):
                cell.block = i

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

    def finished(self):
        correct = True
        list = []
        for x in range(3):
            for i in range(9):
                if correct:
                    if x == 0:
                        list = self.block(i)
                    elif x == 1:
                        list = self.row(i)
                    elif x == 2:
                        list == self.column(i)
                    numbers = []
                    for cell in list:
                        if cell.value in numbers or cell.value == 0:
                            correct = False
                        else:
                            numbers.append(cell.value)
        print correct

    def check_possible(self, list):
        numbers = []
        effect = False
        for cell in list:
            if cell.value > 0:
                numbers.append(cell.value)
        for cell in list:
            removed = cell.remove(numbers, True)
            if removed:
                effect = True
        return effect

    def direct_place(self):
        placed = False
        for row in self.puzzle:
            for cell in row:
                if cell.value == 0 and len(cell.possible) == 1:
                    cell.value = cell.possible[0]
                    placed = True
                    print cell.possible
        print game
        return placed

    def hidden_singles(self):
        placed = False
        list = []
        for x in range(3):
            for y in range(9):
                if x == 0:
                    list = self.block(y)
                if x == 1:
                    list = self.row(y)
                if x == 2:
                    list = self.column(y)
                for i in range(1, 10):
                    possible = []
                    for cell in list:
                        if cell.value == 0 and i in cell.possible:
                            possible.append(cell)
                    if len(possible) == 1:
                        possible[0].value = i
                        self.check_possible(self.row(y))
                        self.check_possible(self.column(y))
                        self.check_possible(self.block(y))
                        placed = True
        print game
        return placed

    def naked_doubles(self, list):
        # naked doubles
        effect = False
        for combo in possible_doubles:
            cells = []
            for cell in list:
                if cell.value == 0 and cell.possible == combo:
                    cells.append(cell)
            if len(cells) == 2:
                for cell in list:
                    if cell not in cells:
                        removed = cell.remove(combo, True)
                        if removed:
                            effect = True
        return effect

    def hidden_doubles(self, list):
        effect = False
        for combo in possible_doubles:
            cells = []
            for cell in list:
                if cell.value == 0:
                    if combo[0] in cell.possible or combo[1] in cell.possible:
                        cells.append(cell)
            if len(cells) == 2:
                hidden_double = True
                for cell in cells:
                    if combo[0] not in cell.possible or combo[1] not in cell.possible:
                        hidden_double = False
                if hidden_double:
                    for cell in cells:
                        for i in range(1, 10):
                            if i not in combo and i in cell.possible:
                                removed = cell.remove(i, True)
                                if removed:
                                    effect = True
        return effect


    def naked_triples(self, list):
        # naked triples
        effect = False
        for triple in possible_triples:
            cells = []
            numbers = []
            for cell in list:
                if cell.value == 0 and len(cell.possible) <= 3:
                    if triple[0] in cell.possible or triple[1] in cell.possible or triple[2] in cell.possible:
                        cells.append(cell)
            for cell in list:
                if cell in cells:
                    for num in cell.possible:
                        if cell in cells:
                            if num not in triple:
                                cells.remove(cell)
            if len(cells) == 3:
                for num in triple:
                    for cell in cells:
                        if num in cell.possible and num not in numbers:
                            numbers.append(num)
                if numbers == triple:
                    for cell in list:
                        if cell not in cells:
                            removed = cell.remove(triple, True)
                            if removed and not effect:
                                effect = True
        return effect

    def hidden_triples(self, list):
        effect = False
        for triple in possible_triples:
            cells = []
            for cell in list:
                if cell.value == 0:
                    if triple[0] in cell.possible or triple[1] in cell.possible or triple[2] in cell.possible:
                        cells.append(cell)
            if len(cells) == 3:
                numbers = []
                for num in triple:
                    for cell in cells:
                        if num in cell.possible and num not in numbers:
                            numbers.append(num)
                if numbers == triple:
                    for cell in cells:
                        for i in range(1, 10):
                            if i not in triple and i in cell.possible:
                                removed = cell.remove(i, True)
                                if removed:
                                    effect = True
        return effect

    def intersection_removal(self, list, *block):
        effect = False
        for i in range(1, 9):
            cells = []
            for cell in list:
                if cell.value == 0 and i in cell.possible:
                    cells.append(cell)
            if len(cells) == 2 or len(cells) == 3:
                if block:
                    row = []
                    for cell in cells:
                        if cell.row not in row:
                            row.append(cell.row)
                    if len(row) == 1:
                        for cell in self.row(row[0]):
                            if cell not in cells and cell.value == 0:
                                if cell.remove(i, True):
                                    effect = True
                    column = []
                    for cell in cells:
                        if cell.column not in column:
                            column.append(cell.column)
                    if len(column) == 1:
                        for cell in self.column(column[0]):
                            if cell not in cells and cell.value == 0:
                                if cell.remove(i, True):
                                    effect = True
                else:
                    block = []
                    for cell in cells:
                        if cell.block not in block:
                            block.append(cell.block)
                    if len(block) == 1:
                        for cell in self.block(block[0]):
                            if cell not in cells and cell.value == 0:
                                if cell.remove(i, True):
                                    effect = True
        return effect

    def check_multiple_solutions(self):
        cells = []
        for row in self.puzzle:
            for cell in row:
                if cell.value == 0:
                    cells.append(cell)
        if len(cells) >= 4:
            for triple in possible_triples:
                multiple_solutions = True
                for cell in cells:
                    for number in cell.possible:
                        if number not in triple:
                            multiple_solutions = False
                if multiple_solutions:
                    cells[0].value = cells[0].possible[0]
                    return True

    def solve(self):
        progress = True
        while progress:
            progress = False
            for i in range(9):
                self.check_possible(self.row(i))
                self.check_possible(self.column(i))
                self.check_possible(self.block(i))
            progress = self.direct_place()
            if not progress:
                progress = self.hidden_singles()
                if not progress:
                    for i in range(9):
                        effect1 = self.naked_doubles(self.block(i))
                        effect2 = self.naked_doubles(self.row(i))
                        effect3 = self.naked_doubles(self.column(i))
                        if effect1 or effect2 or effect3:
                            progress = True
                    if not progress:
                        for i in range(9):
                            effect1 = self.naked_triples(self.block(i))
                            effect2 = self.naked_triples(self.row(i))
                            effect3 = self.naked_triples(self.column(i))
                            if effect1 or effect2 or effect3:
                                progress = True
                        if not progress:
                            for i in range(9):
                                effect1 = self.hidden_doubles(self.block(i))
                                effect2 = self.hidden_doubles(self.row(i))
                                effect3 = self.hidden_doubles(self.column(i))
                                if effect1 or effect2 or effect3:
                                    progress = True
                            if not progress:
                                for i in range(9):
                                    effect1 = self.hidden_triples(self.block(i))
                                    effect2 = self.hidden_triples(self.row(i))
                                    effect3 = self.hidden_triples(self.column(i))
                                    if effect1 or effect2 or effect3:
                                        progress = True
                                    if not progress:
                                        for i in range(9):
                                            effect1 = self.intersection_removal(self.block(i), True)
                                            effect2 = self.intersection_removal(self.row(i))
                                            effect3 = self.intersection_removal(self.column(i))
                                            if effect1 or effect2 or effect3:
                                                progress = True
                                            # if not progress:
                                            #     progress = self.check_multiple_solutions()


class Cell:

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.block = 0
        self.possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if self.value > 0:
            self.possible = []

    def __str__(self):
        return str(self.value)

    def remove(self, x, *does_return):
        effect = False
        if type(x) is list:
            for i in x:
                if i in self.possible:
                    self.possible.remove(i)
                    effect = True
        else:
            if x in self.possible:
                self.possible.remove(x)
                effect = True

        if does_return:
            return effect

possible_doubles = gen_possible_combos(2)
possible_triples = gen_possible_combos(3)
game = Manager()
game.solve()
game.finished()
