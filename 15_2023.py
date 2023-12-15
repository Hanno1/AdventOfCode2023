import helperfunctions as hc

def preprocess_data(data):
    data = data[0].split(',')
    return data

def first_task():
    data = preprocess_data(hc.read_file_line('15_2023'))
    # print(data)
    # data = 'HASH'
    sum_ = 0
    for line in data:
        line_sum = 0
        for entry in line:
            line_sum += ord(entry)
            line_sum *= 17
            line_sum %= 256
        sum_ += line_sum
    print(sum_)

def HASH_ALG(data):
    line_sum = 0
    for entry in data:
        line_sum += ord(entry)
        line_sum *= 17
        line_sum %= 256
    return line_sum

def second_task():
    data = preprocess_data(hc.read_file_line('15_2023'))
    current_lenses = {}
    current_focallengths = {}
    for line in data:
        if '=' in line:
            # add new lens to the end
            # get box to add:
            split_line = line.split('=')
            box_text = split_line[0]
            box = HASH_ALG(split_line[0]) + 1
            focal_length = int(split_line[1])
            if box in current_lenses:
                # if there is already a lens in the box with the same label
                if box_text in current_lenses[box]:
                    index = current_lenses[box].index(box_text)
                    current_focallengths[box][index] = focal_length
                else:
                    current_lenses[box].append(box_text)
                    current_focallengths[box].append(focal_length)
            else:
                current_lenses[box] = [box_text]
                current_focallengths[box] = [focal_length]
        elif '-' in line:
            # remove lens from box
            # get box to remove from:
            split_line = line.split('-')
            box_text = split_line[0]
            box = HASH_ALG(split_line[0]) + 1
            if box in current_lenses:
                if box_text in current_lenses[box]:
                    index = current_lenses[box].index(box_text)
                    current_lenses[box].pop(index)
                    current_focallengths[box].pop(index)
    sum_ = 0
    for fl in current_focallengths:
        slot = 1
        values = current_focallengths[fl]
        for value in values:
            sum_ += fl * slot * value
            slot += 1
    print(sum_)


# first_task()
# print(HASH_ALG('qp'))
second_task()