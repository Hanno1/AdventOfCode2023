import helperfunctions as hc

def preprocess_data(data):
    matrix = {}
    for line in data:
        g = line.split(':')
        game_number = int(g[0].split(' ')[1])
        mat_line = {'red': 0, 'green': 0, 'blue': 0}

        rest_line = g[1].split(';')
        for game in rest_line:
            restline_ = game.split(',')
            for el in restline_:
                el = el.split(' ')[1:]

                color = el[1].replace(';', '')
                number = int(el[0])
                if mat_line[color] < number:
                    mat_line[color] = number

        matrix[game_number] = mat_line
    return matrix

def first_task():
    # 1. Read in the data
    data = hc.read_file_line('02_2023')
    mat = preprocess_data(data)
    
    game_sum = 0
    for game_entry in mat.keys():
        balls = mat[game_entry]
        if balls['red'] <= 12 and balls['green'] <= 13 and balls['blue'] <= 14:
            game_sum += game_entry
            print(game_entry, balls)
    print(game_sum)

def second_task():
    # 1. Read in the data
    data = hc.read_file_line('02_2023')
    mat = preprocess_data(data)
    
    game_sum = 0
    for game_entry in mat.keys():
        # print(game_entry, balls)
        game_sum += mat[game_entry]['red'] * mat[game_entry]['green'] * mat[game_entry]['blue']
    print(game_sum)

# first_task()
second_task()