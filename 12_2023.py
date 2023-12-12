import helperfunctions as hc

def preprocess(data):
    mat = []
    for line in data:
        split = line.split(' ')
        mat.append((split[0], [int(e) for e in split[1].split(',')]))
    return mat

def check_line(line, broken_springs):
    broken_index = 0
    hash_counter = 0
    for el in line:
        if el == '?':
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

            # print(new_line_1, check_line(new_line_1, broken_springs))
            # print(new_line_2, check_line(new_line_2, broken_springs))
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

def unfold(line):
    springs = line[0]
    new_springs = ''
    numbers = line[1]
    new_numbers = []
    for _ in range(5):
        new_springs += springs + '?'
        new_numbers += numbers
    new_springs = new_springs[:-1]
    return (new_springs, new_numbers)


def second_task():
    data = hc.read_file_line('12_2023')
    mat = preprocess(data)

    # unfold paper
    new_mat = []
    for line in mat:
        new_mat.append(unfold(line))
    mat = new_mat
    sum_ = 0
    counter = 0
    for line in mat:
        print(f'starting line {counter + 1}')
        res = fill_springs(line[0], line[1])
        # print(f'current line {line}, result: {res}')
        sum_ += res
        counter += 1
    print(sum_)

# first_task()
second_task()
