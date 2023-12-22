import helperfunctions as hc
import copy

def preprocess(data):
    cmds = []
    for line in data:
        line_split = line.split(' ')
        cmds.append((line_split[0], int(line_split[1])))
    return cmds

def dig(cmds):
    digged_places = []
    current_point = [0, 0]
    for direction, steps in cmds:
        current_x, current_y = current_point
        if direction == 'L':
            for i in range(steps):
                digged_places.append((current_x - i, current_y))
            current_point[0] -= steps
        elif direction == 'R':
            for i in range(steps):
                digged_places.append((current_x + i, current_y))
            current_point[0] += steps
        elif direction == 'U':
            for i in range(steps):
                digged_places.append((current_x, current_y + i))
            current_point[1] += steps
        elif direction == 'D':
            for i in range(steps):
                digged_places.append((current_x, current_y - i))
            current_point[1] -= steps
    return digged_places

def dig_interior(digged_places):
    mat = draw_digs(digged_places, get_mat=True)
    finished = False
    for j in range(len(mat) // 4, len(mat)):
        if finished:
            break
        for i in range(len(mat[j])):
            if mat[j][i] == '#' and mat[j][i + 1] == '.':
                starting_pos = (j, i + 1)
                finished = True
                break
    current_positions = [starting_pos]
    while current_positions:
        new_positions = []
        for x, y in current_positions:
            if mat[x + 1][y] != '#':
                mat[x + 1][y] = '#'
                new_positions.append((x + 1, y))
            if mat[x - 1][y] != '#':
                mat[x - 1][y] = '#'
                new_positions.append((x - 1, y))
            if mat[x][y + 1] != '#':
                mat[x][y + 1] = '#'
                new_positions.append((x, y + 1))
            if mat[x][y - 1] != '#':
                mat[x][y - 1] = '#'
                new_positions.append((x, y - 1))
        current_positions = new_positions
    return sum(mat, []).count('#')

def draw_digs(digged_places, get_mat = False):
    min_x = min([x for x, _ in digged_places])
    max_x = max([x for x, _ in digged_places])
    min_y = min([y for _, y in digged_places])
    max_y = max([y for _, y in digged_places])
    mat = [
        ['.' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)
    ]

    for x, y in digged_places:
        mat[y - min_y][x - min_x] = '#'

    if get_mat:
        return mat

    for line in mat:
        print(''.join(line[0:150]))

    return sum(mat, []).count('#')

def first_task():
    data = hc.read_file_line("18_2023")
    cmds = preprocess(data)
    digged = dig(cmds)
    print('finished digging outside')
    # print(draw_digs(digged))
    digged = dig_interior(digged)
    print(digged)
    print('finished digging inside')
    # print(draw_digs(digged))

first_task()