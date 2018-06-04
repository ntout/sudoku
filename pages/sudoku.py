import numpy as np
from random import choice, randint


def get_column(matrix):
    transpose = [[row[i] for row in matrix] for i in range(9)]
    return transpose


def print_board(board):
    for row in board:
        print(*row)


values = {
    0: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    1: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    2: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    3: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    4: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    5: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    6: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    7: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
    8: {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []},
}


def make_sections(arr):
    one = arr[0:3, 0:3]
    two = arr[0:3, 3:6]
    three = arr[0:3, 6:9]
    four = arr[3:6, 0:3]
    five = arr[3:6, 3:6]
    six = arr[3:6, 6:9]
    seven = arr[6:9, 0:3]
    eight = arr[6:9, 3:6]
    nine = arr[6:9, 6:9]
    section = [one, two, three, four, five, six, seven, eight, nine]
    return section


def fill_number(board):
    column = get_column(board)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for n in range(1, 9+1):
                    if n not in board[i] and n not in column[j] and n not in section_num(make_sections(board), i, j):
                        values[i][j].append(n)
                if len(values[i][j]) == 1:
                    board[i][j] = values[i][j].pop()
    return board


def section_num(lst, i, j):
    if i <= 2:
        if j <= 2:
            return lst[0]
        elif j <= 5:
            return lst[1]
        elif j <= 8:
            return lst[2]
    elif i <= 5:
        if j <= 2:
            return lst[3]
        elif j <= 5:
            return lst[4]
        elif j <= 8:
            return lst[5]
    elif i <= 8:
        if j <= 2:
            return lst[6]
        elif j <= 5:
            return lst[7]
        elif j <= 8:
            return lst[8]


def clear_values(dic):
    for row in dic:
        for i in dic[row]:
            dic[row][i].clear()
    return dic


def initial_fill(arr):
    while (arr == 0).sum() != 0:
        check = (arr == 0).sum()
        clear_values(values)
        fill_number(arr)
        if check == (arr == 0).sum():
            break
    return arr


def solver(arr):
    count = 0
    initial_fill(arr)
    if (arr == 0).sum() == 0:
        return arr
    while True:
        temp = arr.copy()
        col = get_column(temp)
        for i in range(9):
            for j in range(9):
                if temp[i][j] == 0 and len(values[i][j]) > 0:
                    n = choice(values[i][j])
                    while len(values[i][j]) > 1 and n in temp[i] and n in col[j] and n in section_num(make_sections(temp), i, j):
                        n = choice(values[i][j])
                    temp[i][j] = n
                initial_fill(temp)
            if 0 in temp[i]:
                break
        if (temp == 0).sum() == 0:
            return temp
        count += 1


def row_complete(row):
    if len(set(row)) == 9:
        return True
    return False


def check_puzzle(arr):
    for row in arr:
        if len(set(row)) != 9:
            return print('nope row: {}'.format(row))
    for col in get_column(arr):
        if len(set(col)) != 9:
            return print('nope col: {}'.format(col))


def array_to_string(arr):
    str_puz = ''
    for row in arr:
        for i in row:
            str_puz += str(i)
    return str_puz


def string_to_array(string):
    if len(string) != 81:
        return
    arr = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    c = 0
    for i in range(9):
        for j in range(9):
            arr[i][j] = int(string[c])
            c += 1
    return arr


def replace_char_str(string, char, index):
    s = list(string)
    s[index] = char
    return "".join(s)


def verify_sudoku(string):
    if len(string) != 81:
        return False
    temp = string_to_array(string)
    col = get_column(temp)
    for i in range(9):
        for j in range(9):
            if temp[i][j] != 0:
                if (temp[i] == temp[i][j]).sum() > 1:
                    return False
                elif col[j].count(temp[i][j]) > 1:
                    return False
                elif (section_num(make_sections(temp), i, j) == temp[i][j]).sum() > 1:
                    return False
    return True


def fill_blank_puzzle():
    string = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    puzzle = string_to_array(string)
    puzzle_solved = solver(puzzle)
    return array_to_string(puzzle_solved)


def create_sudoku(filled_string):
    filled_list = list(filled_string)
    num_removed = randint(23, 32)
    print(81 - num_removed * 2)
    for n in range(num_removed):
        n += 1
        i = randint(0, 39)
        while filled_list[i] == '0':
            i = randint(0, 39)
        filled_list[i] = '0'
        filled_list[80 - i] = '0'
    return "".join(filled_list)


if __name__ == '__main__':
    # sud3 = '304000000270463108010090003720000000000006900059184000907000302182300400540600070'
    # print_board(solver(string_to_array(sud3)))
    # solver(sud1)
    # solver(puzzle)
    # solver(sud2)
    # print(create_sudoku())
    print(create_sudoku(fill_blank_puzzle()))
