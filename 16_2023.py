import helperfunctions as hc

def preprocess_data(data):
    mat = []
    for line in data:
        current_line = []
        for el in line:
            current_line.append(el)
        mat.append(current_line)
    return mat

def get_next_pos(mat, beam_pos, beam_dir):
    if beam_dir == 'r':
        if beam_pos[1] == len(mat[0]) - 1:
            return []
        next_pos = [beam_pos[0], beam_pos[1] + 1]
    elif beam_dir == 'l':
        if beam_pos[1] == 0:
            return []
        next_pos = [beam_pos[0], beam_pos[1] - 1]
    elif beam_dir == 'u':
        if beam_pos[0] == 0:
            return []
        next_pos = [beam_pos[0] - 1, beam_pos[1]]
    elif beam_dir == 'd':
        if beam_pos[0] == len(mat) - 1:
            return []
        next_pos = [beam_pos[0] + 1, beam_pos[1]]
    else:
        raise Exception(f'Unknown beam direction: {beam_dir}')
    return next_pos

def move_beams(mat, beam_pos, beam_dir):
    # move beam one tile in the matrix to the new position
    current_pos = mat[beam_pos[0]][beam_pos[1]]
    
    if current_pos == '.':
        # just continue
        r = [[get_next_pos(mat, beam_pos, beam_dir), beam_dir]]
    elif current_pos == '/':
        if beam_dir == 'r':
            r = [[get_next_pos(mat, beam_pos, 'u'), 'u']]
        elif beam_dir == 'l':
            r = [[get_next_pos(mat, beam_pos, 'd'), 'd']]
        elif beam_dir == 'u':
            r = [[get_next_pos(mat, beam_pos, 'r'), 'r']]
        elif beam_dir == 'd':
            r = [[get_next_pos(mat, beam_pos, 'l'), 'l']]
    elif current_pos == '\\':
        if beam_dir == 'r':
            r = [[get_next_pos(mat, beam_pos, 'd'), 'd']]
        elif beam_dir == 'l':
            r = [[get_next_pos(mat, beam_pos, 'u'), 'u']]
        elif beam_dir == 'u':
            r = [[get_next_pos(mat, beam_pos, 'l'), 'l']]
        elif beam_dir == 'd':
            r = [[get_next_pos(mat, beam_pos, 'r'), 'r']]
    elif current_pos == '|':
        if beam_dir == 'u' or beam_dir == 'd':
            r = [[get_next_pos(mat, beam_pos, beam_dir), beam_dir]]
        else:
            r = [
                [get_next_pos(mat, beam_pos, 'u'), 'u'],
                [get_next_pos(mat, beam_pos, 'd'), 'd']
            ]
    elif current_pos == '-':
        if beam_dir == 'r' or beam_dir == 'l':
            r = [[get_next_pos(mat, beam_pos, beam_dir), beam_dir]]
        else:
            r = [
                [get_next_pos(mat, beam_pos, 'r'), 'r'],
                [get_next_pos(mat, beam_pos, 'l'), 'l']
            ]
    else:
        raise Exception(f'Unknown matrix pos {current_pos} at {beam_pos}')
    act_r = []
    for el in r:
        if el[0] != []:
            act_r.append(el)
    return act_r

def start_beam(mat, beam_pos, beam_dir):
    # start beam in upper left corner
    current_beams = [[beam_pos, beam_dir]]
    beam_save_pos = []
    while current_beams:
        # print(f'current beams: {current_beams}')
        new_beams = []
        for beam in current_beams:
            if beam in beam_save_pos:
                continue
            # move beam
            new_beams += move_beams(mat, beam[0], beam[1])
        beam_save_pos += current_beams
        current_beams = new_beams

    unique_pos = []
    for el in beam_save_pos:
        if el[0] not in unique_pos:
            unique_pos.append(el[0])
    return len(unique_pos)

def first_task():
    data = hc.read_file_line("16_2023")
    mat = preprocess_data(data)
    beam_pos = [0, 0]
    beam_dir = 'r'
    r = start_beam(mat, beam_pos, beam_dir)
    print(r)

def second_task():
    data = hc.read_file_line("16_2023")
    mat = preprocess_data(data)
    start_positions = []
    for i in range(len(mat)):
        start_positions.append([[i, 0], 'r'])
        start_positions.append([[i, len(mat) - 1], 'l'])
    for i in range(len(mat[0])):
        start_positions.append([[0, i], 'd'])
        start_positions.append([[len(mat[0]) - 1, i], 'u'])
    max_r = 0
    counter = 0
    for pos in start_positions:
        print(f'starting pos {counter}, current max: {max_r}')
        r = start_beam(mat, pos[0], pos[1])
        if r > max_r:
            max_r = r
        counter += 1
    print(max_r)

# first_task()
second_task()
