import helperfunctions as hc

NUMBERS_TO_DIR = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

def preprocess(data):
    cmds = []
    for line in data:
        line_split = line.split(' ')
        cmds.append((line_split[0], int(line_split[1])))
    return cmds

def preprocess2(data):
    cmds = []
    for line in data:
        hex_number = line.split(' ')[-1].replace('(', '').replace(')', '')
        direction = NUMBERS_TO_DIR[int(hex_number[-1])]
        cmds.append((direction, int(hex_number[1:-1], 16)))
    return cmds

def get_lines(cmds):
    hor_lines = []
    ver_lines = []
    current_pos = [0, 0]
    for cmd in cmds:
        direction = cmd[0]
        steps = cmd[1]
        if direction == 'R':
            hor_lines.append([(current_pos[0], current_pos[1]), (current_pos[0] + steps, current_pos[1])])
            current_pos[0] += steps
        elif direction == 'L':
            hor_lines.append([(current_pos[0], current_pos[1]), (current_pos[0] - steps, current_pos[1])])
            current_pos[0] -= steps
        elif direction == 'U':
            ver_lines.append([(current_pos[0], current_pos[1]), (current_pos[0], current_pos[1] + steps)])
            current_pos[1] += steps
        elif direction == 'D':
            ver_lines.append([(current_pos[0], current_pos[1]), (current_pos[0], current_pos[1] - steps)])
            current_pos[1] -= steps
    return [hor_lines, ver_lines]

def first_task():
    data = hc.read_file_line("18_2023")
    cmds = preprocess(data)
    lines = get_lines(cmds)
    ar = hc.get_area(lines)
    print(ar)

def second_task():
    data = hc.read_file_line("18_2023")
    cmds = preprocess2(data)
    lines = get_lines(cmds)
    ar = hc.get_area(lines)
    print(ar)

# first_task()
second_task()