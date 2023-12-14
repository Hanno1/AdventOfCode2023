import helperfunctions as hc

def preprocess(data):
    mat = []
    for line in data:
        split = line.split(' ')
        mat.append((split[0], [int(e) for e in split[1].split(',')]))
    return mat

def check_line(line, broken_springs, springs_count):
    broken_index = 0
    hash_counter = 0
    if line.count('#') > springs_count:
        return False
    counter = 0
    for el in line:
        if el == '?':
            rest_length = len(line) - counter
            rest_springs = sum(broken_springs[broken_index:])
            return True
        if el == '.':
            if hash_counter > 0:
                if broken_index == len(broken_springs):
                    return False
                if hash_counter != broken_springs[broken_index]:
                    return False
                else:
                    hash_counter = 0
                    broken_index += 1
            continue
        elif el == '#':
            hash_counter += 1
            if broken_index == len(broken_springs):
                return False
            if hash_counter > broken_springs[broken_index]:
                return False
        counter += 1
    if hash_counter > 0:
        if broken_index == len(broken_springs):
            return False
        if hash_counter != broken_springs[broken_index]:
            return False
        else:
            hash_counter = 0
            broken_index += 1
    if broken_index != len(broken_springs):
        return False
    return True
    
def fill_springs(line, broken_springs):
    pos = 0
    done = True

    for i in range(len(line)):
        if line[i] == '?':
            new_line_1 = line[:i] + '.' + line[i+1:]
            new_line_2 = line[:i] + '#' + line[i+1:]
            # check if line possible
            if check_line(new_line_1, broken_springs):
                pos += fill_springs(new_line_1, broken_springs)
            if check_line(new_line_2, broken_springs):
                pos += fill_springs(new_line_2, broken_springs)
            done = False
            break
    if done:
        # print(line)
        return 1
    return pos

def first_task():
    data = hc.read_file_line('12_2023')
    mat = preprocess(data)

    sum_ = 0
    for line in mat:
        res = fill_springs(line[0], line[1])
        # print(f'current line {line}, result: {res}')
        sum_ += res
    print(sum_)
    # line = ('?###????????', [3, 2, 1])
    # print(fill_springs(line[0], line[1]))

def unfold_springs(line):
    springs = line[0]
    new_springs = ''
    numbers = line[1]
    for _ in range(5):
        new_springs += springs + '?'
    new_springs = new_springs[:-1]
    return (new_springs, numbers)

def unfold_numbers(line):
    springs = line[0]
    numbers = line[1]
    new_numbers = []
    for _ in range(5):
        new_numbers += numbers
    return (springs, new_numbers)

def fit(unique_el, springs):
    # try fitting springs into the unique_el
    # original spring and not folded
    def fill_spring(current_spring):
        pos = []
        if current_spring.count('?') == 0:
            return [current_spring]
        current_spring_1 = current_spring.replace('?', '#', 1)
        f1 = fill_spring(current_spring_1)
        if f1 != []:
            pos += f1
        current_spring_2 = current_spring.replace('?', '.', 1)
        f2 = fill_spring(current_spring_2)
        if f2 != []:
            pos += f2
        return pos
    possibilities = fill_spring(unique_el)
    print(unique_el, possibilities)

def second_task():
    data = hc.read_file_line('12_2023')
    mat = preprocess(data)

    # unfold paper
    new_mat = []
    for line in mat:
        new_mat.append(unfold_springs(line))
    mat = new_mat

    line = mat[1]
    print(line)
    splited_line = line[0].split('.')
    splited_line = [e for e in splited_line if e != '']
    unique_els = set(splited_line)
    for unique_el in unique_els:
        fit(unique_el, line[1])

# first_task()
second_task()
