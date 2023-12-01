import helperfunctions as hc
import math

number_strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
number_strings_to_int = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                         "six": 6, "seven": 7, "eight": 8, "nine": 9}

def get_numbers(line):
    first = None
    first_index = math.inf
    last = None
    last_index = -1
    counter = 0
    for char in line:
        if char.isdigit():
            if first is None:
                first = char
                first_index = counter
            last = char
            last_index = counter
        counter += 1
    return first, first_index, last, last_index


def first_task():
    # 1. Read in the data
    data = hc.read_file_line('01_2023')
    complete_sum = 0
    for line in data:
        first, _, last, _ = get_numbers(line)
        complete_sum += int(first + last)
    print(complete_sum)

def get_numbers_string(line):
    first = None
    first_index = math.inf
    last = None
    last_index = -1
    for n in number_strings:
        if n in line:
            index = line.find(n)
            if first is None or index < first_index:
                first = n
                first_index = index
            index = line.rfind(n)
            if last is None or index > last_index:
                last = n
                last_index = index
    _first, _first_index, _last, _last_index = get_numbers(line)
    if _first_index < first_index:
        first = _first
    else:
        first = number_strings_to_int[first]
    if _last_index > last_index:
        last = _last
    else:
        last = number_strings_to_int[last]
    return str(first), str(last)

def second_task():
    # 1. Read in the data
    data = hc.read_file_line('01_2023')
    complete_sum = 0
    line_counter = 0
    for line in data:
        first, last = get_numbers_string(line)
        line_counter += 1
        complete_sum += int(first + last)
    print(complete_sum)


# first_task()
# second_task()
