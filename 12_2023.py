import helperfunctions as hc
import math

def preprocess(data):
    mat = []
    for line in data:
        split = line.split(' ')
        mat.append([split[0], [int(e) for e in split[1].split(',')]])
    return mat

def check_line(line, broken_springs, springs_count = math.inf):
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

def unfold_line(line):
    new_springs = unfold_springs(line)
    new_numbers = unfold_numbers(line)
    return (new_springs, new_numbers)

def fit_springs(springs, numbers):
    if len(springs) < len(numbers) + sum(numbers) - 1:
        return 0
    possibilities = 0
    if len(numbers) == 0:
        # just fit only points
        if springs.count('#') == 0:
            return 1
        return 0
    next_spring = springs[0]
    next_number = numbers[0]
    # we have a question mark a # or a . in front of us
    if next_spring == '.':
        # go to next ? or #
        next_index = min(springs.index('#'), springs.index('?'))
        possibilities += fit_springs(springs[next_index:], numbers)
    elif next_spring == '#':
        # check if we can fit the next number
        part_string = springs[:next_number]
        if '.' in part_string:
            return 0
        if len(springs) == next_number:
            if len(numbers) == 1:
                return 1
            return 0
        possibilities += fill_springs(springs[next_number + 1:], numbers[1:])
    else:
        # question mark
        # either . or #
        # case of a point
        possibilities += fill_springs(springs[1:], numbers)
        springs = springs.replace('?', '#', 1)
        possibilities += fill_springs(springs, numbers)
    return possibilities

def solve_line(line):
    springs = line[0]
    numbers = line[1]

    pos = fit_springs(springs[0], numbers[1])
    print(f'Result of the line is {pos}')
    return pos

def second_task():
    data = preprocess(hc.read_file_line('12_2023'))
    unfold_lines = []
    for line in data:
        unfold_lines.append(unfold_line(line))
    sum_ = 0
    counter = 0
    for line in unfold_lines:
        print(f'Starting line {counter}')
        sum_ += solve_line(line)
        counter += 1
    print(sum_)

# first_task()
second_task()
