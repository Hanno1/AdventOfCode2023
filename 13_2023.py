import helperfunctions as hc

def preprocess(data):
    mat = []
    tmp_line = []
    for line in data:
        if line == '':
            mat.append(tmp_line)
            tmp_line = []
            continue
        tmp_line.append(line)
    mat.append(tmp_line)
    return mat

def get_horizantal(mat):
    # test for mirror horizontal
    for counter in range(1, len(mat)):
        top_rows = [row for i, row in enumerate(mat) if i < counter]
        bot_rows = [row for i, row in enumerate(mat) if i >= counter]
        if len(top_rows) > len(bot_rows):
            top_rows = top_rows[len(top_rows) - len(bot_rows):]
        elif len(top_rows) < len(bot_rows):
            bot_rows = bot_rows[:len(top_rows)]
        bot_rows = bot_rows[::-1]
        # print(counter, top_rows, bot_rows)
        if top_rows == bot_rows:
            return counter
    return -1

def get_vertical(mat):
    for counter in range(1, len(mat[0])):
        left_cols = [''.join([row[i] for row in mat]) for i in range(counter)]
        right_cols = [''.join([row[i] for row in mat]) for i in range(counter, len(mat[0]))]

        if len(left_cols) > len(right_cols):
            left_cols = left_cols[len(left_cols) - len(right_cols):]
        elif len(left_cols) < len(right_cols):
            right_cols = right_cols[:len(left_cols)]
        right_cols = right_cols[::-1]
        if left_cols == right_cols:
            return counter
    return -1

def first_task():
    data = hc.read_file_line('13_2023')
    mat = preprocess(data)
    sum_ = 0
    for line in mat:
        res = get_horizantal(line)
        if res != -1:
            sum_ += res * 100
            continue
        res = get_vertical(line)
        if res == -1:
            raise Exception('No solution found')
        sum_ += res
    print(sum_)

def get_horizantal_2(mat):
    # test for mirror horizontal
    for counter in range(1, len(mat)):
        top_rows = [row for i, row in enumerate(mat) if i < counter]
        bot_rows = [row for i, row in enumerate(mat) if i >= counter]
        if len(top_rows) > len(bot_rows):
            top_rows = top_rows[len(top_rows) - len(bot_rows):]
        elif len(top_rows) < len(bot_rows):
            bot_rows = bot_rows[:len(top_rows)]
        bot_rows = bot_rows[::-1]
        # print(counter, top_rows, bot_rows)
        smudge_counter = 0
        for r in range(len(top_rows)):
            r1 = top_rows[r]
            r2 = bot_rows[r]
            if r1 == r2:
                continue
            # different lines -> check for correction
            for c in range(len(r1)):
                if r1[c] == r2[c]:
                    continue
                if r1[c] == '#' and r2[c] == '.' or r1[c] == '.' and r2[c] == '#':
                    smudge_counter += 1
                    if smudge_counter > 1:
                        break
            if smudge_counter > 1:
                break
        if smudge_counter == 1:
            return counter
    return -1

def get_vertical_2(mat):
    for counter in range(1, len(mat[0])):
        left_cols = [''.join([row[i] for row in mat]) for i in range(counter)]
        right_cols = [''.join([row[i] for row in mat]) for i in range(counter, len(mat[0]))]

        if len(left_cols) > len(right_cols):
            left_cols = left_cols[len(left_cols) - len(right_cols):]
        elif len(left_cols) < len(right_cols):
            right_cols = right_cols[:len(left_cols)]
        right_cols = right_cols[::-1]
        smudge_counter = 0
        for c in range(len(left_cols)):
            c1 = left_cols[c]
            c2 = right_cols[c]
            if c1 == c2:
                continue
            # different lines -> check for correction
            for c in range(len(c1)):
                if c1[c] == c2[c]:
                    continue
                if c1[c] == '#' and c2[c] == '.' or c1[c] == '.' and c2[c] == '#':
                    smudge_counter += 1
                    if smudge_counter > 1:
                        break
            if smudge_counter > 1:
                break
        if smudge_counter == 1:
            return counter
    return -1

def second_task():
    data = hc.read_file_line('13_2023')
    mat = preprocess(data)
    sum_ = 0
    for line in mat:
        res = get_horizantal_2(line)
        if res != -1:
            sum_ += res * 100
            continue
        res = get_vertical_2(line)
        if res == -1:
            raise Exception('No solution found')
        sum_ += res
    print(sum_)
    # too low: 35961

# first_task()
second_task()