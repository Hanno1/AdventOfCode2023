import helperfunctions as hc

def preprocess_data(data):
    mat = []
    start_pos = None
    for line in data:
        mat.append([entry for entry in line])
        if line.find('S') != -1:
            start_pos = (len(mat) - 1, line.find('S'))
    return mat, start_pos

def check_pipe_bot(mat, pos, visited):
     row, col = pos
     if row < len(mat) - 1:
        below_el = mat[row + 1][col]
        if below_el in ['|', 'L', 'J'] and [row + 1, col] not in visited:
            return [row + 1, col]
     return None

def check_pipe_top(mat, pos, visited):
    row, col = pos
    if row > 0:
        above_el = mat[row - 1][col]
        if above_el in ['|', '7', 'F'] and [row - 1, col] not in visited:
            return [row - 1, col]
    return None

def check_pipe_left(mat, pos, visited):
    row, col = pos
    if col > 0:
        left_el = mat[row][col - 1]
        if left_el in ['-', 'L', 'F'] and [row, col - 1] not in visited:
            return [row, col - 1]
    return None

def check_pipe_right(mat, pos, visited):
    row, col = pos
    if col < len(mat[0]) - 1:
        right_el = mat[row][col + 1]
        if right_el in ['-', '7', 'J'] and [row, col + 1] not in visited:
            return [row, col + 1]
    return None

def get_possible_positions(mat, pos, visited):
    row, col = pos
    possible_positions = []
    # check current element
    el = mat[row][col]
    if el == 'S':
        # explore all neighbours
        possible_positions = []
        # check top
        if row > 0:
            above_el = mat[row - 1][col]
            if above_el not in ['L', 'J', '-', '.']:
                possible_positions.append([row - 1, col])
        # check bot
        if row < len(mat) - 1:
            below_el = mat[row + 1][col]
            if below_el not in ['7', 'F', '-', '.']:
                possible_positions.append([row + 1, col])
        # check left
        if col > 0:
            left_el = mat[row][col - 1]
            if left_el not in ['7', 'J', '|', '.']:
                possible_positions.append([row, col - 1])
        # check right
        if col < len(mat[0]) - 1:
            right_el = mat[row][col + 1]
            if right_el not in ['L', 'F', '|', '.']:
                possible_positions.append([row, col + 1])
    # check other elements:
    # check if top connection
    if el in ['|', 'L', 'J']:
        res = check_pipe_top(mat, pos, visited)
        if res:
            possible_positions.append(res)
    # check if bot connection
    if el in ['|', '7', 'F']:
        res = check_pipe_bot(mat, pos, visited)
        if res:
            possible_positions.append(res)
    # check if left connection
    if el in ['-', '7', 'J']:
        res = check_pipe_left(mat, pos, visited)
        if res:
            possible_positions.append(res)
    # check if right connection
    if el in ['-', 'L', 'F']:
        res = check_pipe_right(mat, pos, visited)
        if res:
            possible_positions.append(res)
    return possible_positions

def explore_step(mat, current_positions, visited):
    new_positions = []
    for pos in current_positions:
        new_positions += get_possible_positions(mat, pos, visited)
    return new_positions

def explore(mat, start_pos):
    current_positions = [start_pos]
    counter = 0
    visited_pos = []
    while True:
        # print(current_positions)
        new_positions = explore_step(mat, current_positions, visited_pos)
        # check if finished -> one position is doubled
        for el in current_positions:
            if current_positions.count(el) > 1:
                return counter
        counter += 1
        visited_pos = current_positions
        current_positions = new_positions

def first_task():
    data = hc.read_file_line('10_2023')
    mat, s = preprocess_data(data)
    res = explore(mat, s)
    print(res)

def explore_path(mat, start_pos):
    current_positions = [[start_pos[0], start_pos[1]]]
    path_nodes = []
    counter = 0
    visited_pos = []
    while True:
        # print(current_positions)
        new_positions = explore_step(mat, current_positions, visited_pos)
        # check if finished -> one position is doubled
        for el in current_positions:
            path_nodes.append(el)
            if current_positions.count(el) > 1:
                return path_nodes, counter
        counter += 1
        visited_pos = current_positions
        current_positions = new_positions
        # visited_pos += new_positions

def pad_mat(mat):
    # pad mat with '.'
    new_mat = []
    for row in mat:
        new_mat.append(['.'] + row + ['.'])
    new_mat.insert(0, ['.'] * len(new_mat[0]))
    new_mat.append(['.'] * len(new_mat[0]))
    return new_mat

def connected_horizontally(top_symbol, bot_symbol):
    if top_symbol == '7' or top_symbol == 'F' or top_symbol == '|':
        if bot_symbol == 'L' or bot_symbol == 'J' or bot_symbol == '|':
            return True
    return False

def connected_vertically(left_symbol, right_symbol):
    if left_symbol == 'L' or left_symbol == 'F' or left_symbol == '-':
        if right_symbol == '7' or right_symbol == 'J' or right_symbol == '-':
            return True
    return False

def pad_horizontal(mat, path):
    added_points = 0
    new_mat = []
    # path between each line horizontally
    for i in range(len(mat) - 1):
        # add padding line
        new_line = ['.'] * len(mat[0])
        added_points += len(mat[0])
        top_line = mat[i]
        bot_line = mat[i + 1]
        for j in range(len(top_line)):
            if connected_horizontally(top_line[j], bot_line[j]):
                new_line[j] = 'X'
                added_points -= 1
        new_mat.append(mat[i])
        new_mat.append(new_line)

        # update path
        for el in path:
            if el[0] >= len(new_mat) - 1:
                el[0] += 1

    new_mat.append(mat[-1])
    return new_mat, path, added_points

def pad_vertical(mat, path):
    added_points = 0
    new_mat = [[] for _ in range(len(mat))]
    # path between each line vertically
    for i in range(len(mat[0]) - 1):        
        new_column_line = ['.'] * len(mat)
        added_points += len(mat)
        left_column = [row[i] for row in mat]
        right_column = [row[i + 1] for row in mat]
        for j in range(len(left_column)):
            if connected_vertically(left_column[j], right_column[j]):
                new_column_line[j] = 'X'
                added_points -= 1
        for j in range(len(mat)):
            new_mat[j].append(left_column[j])
            new_mat[j].append(new_column_line[j])
        # update path
        for el in path:
            if el[1] >= len(new_mat[0]) - 1:
                el[1] += 1
    
    for j in range(len(new_mat)):
        new_mat[j].append('.')
    return new_mat, path, added_points

def set_start_right(mat, path):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 'S':
                # check if opening to the top
                top = mat[i-1][j] in ['|', '7', 'F'] and [i-1, j] in path
                # check if opening to the bot
                bot = mat[i+1][j] in ['|', 'L', 'J'] and [i+1, j] in path
                # check if opening to the left
                left = mat[i][j-1] in ['-', 'L', 'F'] and [i, j-1] in path
                # check if opening to the right
                right = mat[i][j+1] in ['-', '7', 'J'] and [i, j+1] in path
                if top:
                    if bot:
                        mat[i][j] = '|'
                    elif left:
                        mat[i][j] = 'J'
                    elif right:
                        mat[i][j] = 'L'
                elif bot:
                    if left:
                        mat[i][j] = '7'
                    elif right:
                        mat[i][j] = 'F'
                elif left:
                    if right:
                        mat[i][j] = '-'
                else:
                    raise Exception('No opening found')
                return mat
            
def set_path_right(mat, path):
    for row, col in path:
        mat[row][col] = 'X'
    return mat

def enclosed_counter(mat, points):
    # get starting point at outer conntection components
    row = 0
    col = mat[row].index('.')
    point_counter = 1
    current_positions = [[row, col]]
    visited_pos = []

    while current_positions:
        new_positions = []
        for pos in current_positions:
            r, c = pos
            # expand position
            # move top
            if r > 0 and [r-1, c] not in visited_pos and [r-1, c] not in new_positions and mat[r-1][c] != 'X':
                if mat[r-1][c] != '-':
                    new_positions.append([r-1, c])
                    if mat[r-1][c] == '.':
                        point_counter += 1
            # move bot
            if r < len(mat) - 1 and [r+1, c] not in visited_pos and [r+1, c] not in new_positions and mat[r+1][c] != 'X':
                if mat[r+1][c] != '-':
                    new_positions.append([r+1, c])
                    if mat[r+1][c] == '.':
                        point_counter += 1
            # move left
            if c > 0 and [r, c-1] not in visited_pos and [r, c-1] not in new_positions and mat[r][c-1] != 'X':
                if mat[r][c-1] != '|':
                    new_positions.append([r, c-1])
                    if mat[r][c-1] == '.':
                        point_counter += 1
            # move right
            if c < len(mat[0]) - 1 and [r, c+1] not in visited_pos and [r, c+1] not in new_positions and mat[r][c+1] != 'X':
                if mat[r][c+1] != '|':
                    new_positions.append([r, c+1])
                    if mat[r][c+1] == '.':
                        point_counter += 1
        visited_pos += current_positions
        current_positions = new_positions
    print(points, point_counter)
    print(points - point_counter)


def get_inner_points(mat):
    # get start point
    # start_point = None
    # for row in range(len(mat)):
    #     if 'X' in mat[row]:
    #         first_x = mat[row].index('X')
    #         if first_x != -1:
    #             if mat[row][first_x + 1] == '.':
    #                 start_point = [row, first_x + 1]
    #                 break
    start_point = [45, 29]
    print(mat[start_point[0]][start_point[1]])
    inner_points = 1
    inner_point_list = [start_point]
    current_positions = [start_point]
    visited_pos = []
    while current_positions:
        new_positions = []
        for r,c in current_positions:
            if r>0 and [r-1, c] not in visited_pos and mat[r-1][c] != 'X' and [r-1,c] not in new_positions:
                new_positions.append([r-1, c])
                inner_point_list.append([r-1, c])
                inner_points += 1
            if r<len(mat) - 1 and [r+1, c] not in visited_pos and mat[r+1][c] != 'X' and [r+1,c] not in new_positions:
                new_positions.append([r+1, c])
                inner_point_list.append([r+1, c])
                inner_points += 1
            if c > 0 and [r, c-1] not in visited_pos and mat[r][c-1] != 'X' and [r,c-1] not in new_positions:
                new_positions.append([r, c-1])
                inner_point_list.append([r, c-1])
                inner_points += 1
            if c < len(mat[0]) - 1 and [r, c+1] not in visited_pos and mat[r][c+1] != 'X' and [r,c+1] not in new_positions:
                new_positions.append([r, c+1])
                inner_point_list.append([r, c+1])
                inner_points += 1
        visited_pos += current_positions
        current_positions = new_positions
    
    return inner_point_list

def second_task():
    data = hc.read_file_line('10_2023')
    mat, s = preprocess_data(data)

    mat = pad_mat(mat)
    original_points = 0
    for line in mat:
        original_points += line.count('.')

    s = [s[0] + 1, s[1] + 1]

    path, _ = explore_path(mat, s)
    mat = set_start_right(mat, path)

    mat, path, added_h = pad_horizontal(mat, path)
    mat, path, added_v = pad_vertical(mat, path)

    mat = set_path_right(mat, path)

    inner_points = get_inner_points(mat)

    new_inner_points = []
    for r, c in inner_points:
        if r % 2 == 0 and c % 2 == 0:
            new_inner_points.append([r, c])
    print(len(new_inner_points))

    

# first_task()
second_task()

