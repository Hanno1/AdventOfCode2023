import helperfunctions as hc
import copy

def move_stones_north_1(data):
    rows = len(data)
    first_empty_tile = [-1 for _ in range(len(data[0]))]
    row = 0
    sum_ = 0
    for line in data:
        for col in range(len(line)):
            entry = line[col]
            if entry == '#':
                first_empty_tile[col] = -1
            elif entry == 'O':
                if first_empty_tile[col] != -1:
                    # move stone to first empty tile
                    sum_ += len(data) - first_empty_tile[col]
                    first_empty_tile[col] += 1
                else:
                    # dont move
                    sum_ += rows
            elif entry == '.'and  first_empty_tile[col] == -1:
                first_empty_tile[col] = row
        rows -= 1
        row += 1
    print(sum_)

def first_task():
    data = hc.read_file_line('14_2023')
    round_stones, square_stones, rows, cols = preprocess_data(data)
    round_stones = move_stones_north(round_stones, square_stones, rows, cols)
    print(calculate_load(round_stones, rows, cols))

def preprocess_data(data):
    round_stones = []
    square_stones = []
    total_rows = len(data)
    total_cols = len(data[0])
    for row in range(len(data)):
        for col in range(len(data[row])):
            entry = data[row][col]
            if entry == 'O':
                round_stones.append((row, col))
            elif entry == '#':
                square_stones.append((row, col))
    return round_stones, square_stones, total_rows, total_cols

def move_stones_north(round_stones, square_stones, rows, cols):
    first_empty_tile = [-1 for _ in range(cols)]
    new_round_stones = []
    for row in range(rows):
        for col in range(cols):
            if (row, col) in square_stones:
                first_empty_tile[col] = -1
            elif (row, col) in round_stones:
                if first_empty_tile[col] != -1:
                    # move stone to first empty tile
                    new_round_stones.append((first_empty_tile[col], col))
                    first_empty_tile[col] += 1
                else:
                    # dont move
                    new_round_stones.append((row, col))
            else:
                if first_empty_tile[col] == -1:
                    first_empty_tile[col] = row
    return new_round_stones

def move_stones_south(round_stones, square_stones, rows, cols):
    first_empty_tile = [-1 for _ in range(cols)]
    new_round_stones = []
    for row in range(rows - 1, -1, -1):
        for col in range(cols):
            if (row, col) in square_stones:
                first_empty_tile[col] = -1
            elif (row, col) in round_stones:
                if first_empty_tile[col] != -1:
                    # move stone to first empty tile
                    new_round_stones.append((first_empty_tile[col], col))
                    first_empty_tile[col] -= 1
                else:
                    # dont move
                    new_round_stones.append((row, col))
            else:
                if first_empty_tile[col] == -1:
                    first_empty_tile[col] = row
    return new_round_stones

def move_stones_west(round_stones, square_stones, rows, cols):
    first_empty_tile = [-1 for _ in range(rows)]
    new_round_stones = []
    for col in range(cols):
        for row in range(rows):
            if (row, col) in square_stones:
                first_empty_tile[row] = -1
            elif (row, col) in round_stones:
                if first_empty_tile[row] != -1:
                    # move stone to first empty tile
                    new_round_stones.append((row, first_empty_tile[row]))
                    first_empty_tile[row] += 1
                else:
                    # dont move
                    new_round_stones.append((row, col))
            else:
                if first_empty_tile[row] == -1:
                    first_empty_tile[row] = col
    return new_round_stones

def move_stones_east(round_stones, square_stones, rows, cols):
    first_empty_tile = [-1 for _ in range(rows)]
    new_round_stones = []
    for col in range(cols - 1, -1, -1):
        for row in range(rows):
            if (row, col) in square_stones:
                first_empty_tile[row] = -1
            elif (row, col) in round_stones:
                if first_empty_tile[row] != -1:
                    # move stone to first empty tile
                    new_round_stones.append((row, first_empty_tile[row]))
                    first_empty_tile[row] -= 1
                else:
                    # dont move
                    new_round_stones.append((row, col))
            else:
                if first_empty_tile[row] == -1:
                    first_empty_tile[row] = col
    return new_round_stones

def display_stones(round_stones, square_stones, rows, cols):
    mat = []
    for row in range(rows):
        mat.append(['.' for _ in range(cols)])
        for col in range(cols):
            if (row, col) in round_stones:
                mat[row][col] = 'O'
            elif (row, col) in square_stones:
                mat[row][col] = '#'
    print('-' * 10)
    for line in mat:
        print(''.join(line))

def move_cycle(round_stones, square_stones, rows, cols):

    # O....#....    OOOO.#.O..  OOOO.#O...  .....#....  .....#....
    # O.OO#....#    OO..#....#  OO..#....#  ....#.O..#  ....#...O#
    # .....##...    OO..O##..O  OOO..##O..  O..O.##...  ...OO##...
    # OO.#O....O    O..#.OO...  O..#OO....  O.O#......  .OO#......
    # .O.....O#.    ........#.  ........#.  O.O....O#.  .....OOO#.
    # O.#..O.#.#    ..#....#.#  ..#....#.#  O.#..O.#.#  .O#...O#.#
    # ..O..#O..O    ..O..#.O.O  O....#OO..  O....#....  ....O#....
    # .......O..    ..O.......  O.........  OO....OO..  ......OOOO
    # #....###..    #....###..  #....###..  #O...###..  #...O###..
    # #OO..#....    #....#....  #....#....  #O..O#....  #..OO#....

    new_round_stones = move_stones_north(round_stones, square_stones, rows, cols)
    new_round_stones = move_stones_west(new_round_stones, square_stones, rows, cols)
    new_round_stones = move_stones_south(new_round_stones, square_stones, rows, cols)
    new_round_stones = move_stones_east(new_round_stones, square_stones, rows, cols)
    return new_round_stones

def calculate_load(round_stones, rows, cols):
    load = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) in round_stones:
                load += rows - row
    return load

def second_task():
    data = hc.read_file_line('14_2023')
    round_, square, rows, cols = preprocess_data(data)
    # print(round_)
    r = 1_000_000_000
    save_pos = []
    orig_round = copy.deepcopy(round_)
    cycle_length = 0
    start_pos = None
    for i in range(r):
        save_pos.append(copy.deepcopy(round_))
        print(f'Starting round {i}')
        round_ = move_cycle(round_, square, rows, cols)
        if round_ in save_pos:
            index = save_pos.index(round_)
            print(f'Found round {i}, {index}')
            cycle_length = i - index + 1
            start_pos = index
            break

    # display_stones(round_, square, rows, cols)
    
    round = 0
    round_ = orig_round
    for i in range(start_pos):
        round_ = move_cycle(round_, square, rows, cols)
        round += 1

    # for i in range(1):
    #     for _ in range(cycle_length):
    #         round_ = move_cycle(round_, square, rows, cols)
    #         round += 1
        # display_stones(round_, square, rows, cols)



    round += ((r - start_pos) // cycle_length) * cycle_length
    # round -= cycle_length
    # round -= 10 * cycle_length
    for i in range(r - round):
        round_ = move_cycle(round_, square, rows, cols)
    load = calculate_load(round_, rows, cols)
    print(load)
    
# first_task()
second_task()