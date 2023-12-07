import helperfunctions as hc

GAMES = ['high', 'one', 'two', 'three', 'full_house', 'four', 'five']
CHARS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CHARS_2 = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

def preprocess_data(data):
    mat = {}
    for counter in range(len(data)):
        line = data[counter].split(' ')
        line[1] = int(line[1])
        mat[counter + 1] = line
    return mat

def get_game(values):
    counters = {}
    for value in values:
        if value in counters:
            counters[value] += 1
        else:
            counters[value] = 1
    v = []
    for entry in counters:
        v.append(counters[entry])
    if len(v) == 1:
        return 'five'
    elif len(v) == 2:
        # either full house or four
        if 4 in v:
            return 'four'
        else:
            return 'full_house'
    elif len(v) == 3:
        # either three or two
        if 3 in v:
            return 'three'
        else:
            return 'two'
    elif len(v) == 4:
        return 'one'
    return 'high'

def smaller_relation(game1, game2, use_chars_2=False):
    # returns true if game1 is smaller than game2
    chars_list = CHARS_2 if use_chars_2 else CHARS
    for char in range(5):
        if chars_list.index(game1[char]) < chars_list.index(game2[char]):
            return True
        elif chars_list.index(game1[char]) > chars_list.index(game2[char]):
            return False
    raise ValueError(f"Games are equal, game: {game1, game2}")

def sort_by_values(games, use_chars_2=False):
    for index in range(1, len(games)):
        game = games[index]
        added = False
        for j in range(index, 0, -1):
            if smaller_relation(game[0], games[j - 1][0], use_chars_2):
                games[j] = games[j - 1]
            else:
                games[j] = game
                added = True
                break
        if not added:
            games[0] = game
    return games

def sort_by_game(mat):
    sorted_mat = {entry: [] for entry in GAMES}
    for game in mat:
        values = mat[game]
        result = get_game(values[0])
        sorted_mat[result].append(values)
    return sorted_mat

def first_task():
    data = hc.read_file_line("07_2023")
    mat = preprocess_data(data)
    sorted_1 = sort_by_game(mat)

    res = []
    for game_type in sorted_1:
        res.append(sort_by_values(sorted_1[game_type]))
    summ = 0
    counter = 1
    for line in res:
        for game in line:
            summ += game[1] * counter
            counter += 1
    print(summ)

def get_game_2(values):
    counters = {}
    for value in values:
        if value in counters:
            counters[value] += 1
        else:
            counters[value] = 1
    v = []
    for entry in counters:
        v.append(counters[entry])
    # how many jokers are there?
    counter_jokers = counters['J'] if 'J' in counters else 0
    if len(v) == 1 or (len(v) == 2 and counter_jokers > 0):
        return 'five'
    elif len(v) == 2 or (len(v) == 3 and counter_jokers > 0):
        # either full house or four
        if counter_jokers > 0:
            if counter_jokers == 3 or counter_jokers == 2:
                return 'four'
            else:
                # 1 joker
                if 3 in v:
                    return 'four'
                else:
                    return 'full_house'
        if 4 in v:
            return 'four'
        else:
            return 'full_house'
    elif len(v) == 3 or (len(v) == 4 and counter_jokers > 0):
        # either three or two
        if counter_jokers > 0:
            if counter_jokers == 2:
                return 'three'
            elif counter_jokers == 1 and 2 in v:
                return 'three'
            else:
                return 'two'
        if 3 in v:
            return 'three'
        else:
            return 'two'
    elif len(v) == 4 or counter_jokers > 0:
        return 'one'
    return 'high'

def sort_by_game_2(mat):
    sorted_mat = {entry: [] for entry in GAMES}
    for game in mat:
        values = mat[game]
        result = get_game_2(values[0])
        sorted_mat[result].append(values)
    return sorted_mat

def second_task():
    data = hc.read_file_line("07_2023")
    mat = preprocess_data(data)
    sorted_1 = sort_by_game_2(mat)

    res = []
    for game_type in sorted_1:
        res.append(sort_by_values(sorted_1[game_type], True))
    summ = 0
    counter = 1
    for line in res:
        for game in line:
            summ += game[1] * counter
            counter += 1
    print(summ)

# first_task()
second_task()

