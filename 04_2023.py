import helperfunctions as hc

def preprocess_data(data):
    mat = {}
    for line in data:
        split_line_1 = line.split(":")
        card_number = int(split_line_1[0].split(' ')[-1])
        split_line_2 = split_line_1[1].split('|')
        winning_numbers = list(filter(lambda i: i != '', split_line_2[0].split(' ')))
        actual_numbers = list(filter(lambda i: i != '', split_line_2[1].split(' ')))
        mat[card_number] = [[int(i) for i in winning_numbers], [int(i) for i in actual_numbers], 1]

    return mat

def first_task():
    data = hc.read_file_line("04_2023")
    data = preprocess_data(data)
    
    summ = 0
    for key in data:
        winning, actual, freq = data[key]
        current_win = 0
        for number in winning:
            if number in actual:
                if current_win == 0:
                    current_win = 1
                else:
                    current_win *= 2
        summ += current_win
    print(summ)

def second_task():
    data = hc.read_file_line("04_2023")
    total_cards = len(data)

    data = preprocess_data(data)

    summ = 0
    for key in data:
        winning, actual, freq = data[key]
        summ += freq
        current_win = 0
        for number in winning:
            if number in actual:
                current_win += 1

        index = 1
        while index <= current_win:
            if key + index > total_cards:
                break
            data[key + index][2] += freq
            index += 1

        # print(key)
        # print(f'Round {key}, data: {data}')
    # print(data)
    # wrong??? 9671254
    print(summ)

# first_task()
second_task()