
class Manager:

    def __init__(self):
        # 0 is an empty space
        self.puzzle = []
        self.set_up()

    def __str__(self):
        string = ""
        for row in self.puzzle:
            for space in row:
                string += str(space) + ' '
            string += '\n'
        return string

    def set_up(self):
        puzzle = [[3, 0, 8, 6, 4, 0, 0, 2, 0],
                   [0, 0, 0, 8, 0, 9, 0, 4, 7],
                   [1, 0, 9, 0, 0, 2, 0, 0, 0],
                   [6, 0, 1, 0, 0, 0, 0, 3, 0],
                   [7, 3, 0, 0, 0, 0, 0, 6, 4],
                   [0, 8, 0, 0, 0, 0, 2, 0, 1],
                   [0, 0, 0, 9, 0, 0, 8, 0, 5],
                   [8, 6, 0, 7, 0, 3, 0, 0, 0],
                   [0, 9, 0, 0, 8, 5, 3, 0, 6]]
        x = 0
        for row in puzzle:
            self.puzzle.append([])
            y = 0
            for column in puzzle:
                self.puzzle[x].append(Space(puzzle[x][y], x, y))
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
                    space.possible.remove(number)

    def solve(self):
        running = True
        while running:
            running = False
            for i in range(9):
                self.check_possible(self.row(i))
                self.check_possible(self.column(i))
                self.check_possible(self.block(i))
            for row in self.puzzle:
                for space in row:
                    if space.value == 0:
                        if len(space.possible) == 1:
                            space.value = space.possible[0]
                            running = True
                        print space.possible



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


game = Manager()
game.solve()
print game
