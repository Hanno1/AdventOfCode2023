import helperfunctions as hc

def preprocess_data(data, second=False):
    numbers = []
    symbols = []
    line_counter = 0
    for line in data:
        current_number = ''
        start = None
        char_counter = 0
        for char in line:
            if char.isdigit():
                if current_number == '':
                    start = char_counter
                current_number += char
            elif char == '.':
                if current_number != '':
                    numbers.append((current_number, line_counter, start, char_counter - 1))
                    current_number = ''
            else:
                if current_number != '':
                    numbers.append((current_number, line_counter, start, char_counter - 1))
                    current_number = ''
                if second:
                    symbols.append((char, line_counter, char_counter))
                else:
                    symbols.append((line_counter, char_counter))
            char_counter += 1
        if current_number != '':
            numbers.append((current_number, line_counter, start, char_counter - 1))
        line_counter += 1

    return numbers, symbols

def check_adj(symbols, row, start, end):
    # check top and bottom
    for i in range(start - 1, end + 2):
        for j in [-1, 1]:
            if (row + j, i) in symbols:
                return True
    # check left and right
    if (row, start - 1) in symbols:
        return True
    if (row, end + 1) in symbols:
        return True
    return False

def first_task():
    data = hc.read_file_line("03_2023")
    numbers_, symbols_ = preprocess_data(data)

    # print(symbols_)

    summ = 0
    for n, row, start, end in numbers_:
        # print(n, row, start, end)
        res = check_adj(symbols_, row, start, end)
        if res:
            summ += int(n)

    print(summ)

def check_adj_gears(numbers, row, col):
    # check if gear is star and adjacent to exactly 2 numbers
    adj_numbers = []
    for n, r, start, end in numbers:
        if abs(r - row) <= 1 and start - 1 <= col <= end + 1:
            adj_numbers.append(n)
    if len(adj_numbers) != 2:
        return False
    return adj_numbers

def second_task():
    data = hc.read_file_line("03_2023")
    numbers_, symbols_ = preprocess_data(data, True)

    summ = 0
    for symbol, row, col in symbols_:
        if symbol == '*':
            res = check_adj_gears(numbers_, row, col)
            if res:
                summ += int(res[0]) * int(res[1])
    print(summ)

# first_task()
second_task()