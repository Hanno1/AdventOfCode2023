import helperfunctions as hc

def preprocess_data(data):
    mat = []
    for line in data:
        mat.append(line)
        if line.count('#') == 0:
            mat.append(line)
    # vertical expansion:
    counter = 0
    for i in range(len(mat[0])):
        column = [line[i] for line in data]
        if column.count('#') == 0:
            for j in range(len(mat)):
                mat[j] = mat[j][:i + counter] + '.' + mat[j][i + counter:]
            counter += 1
    return mat

def get_galaxies(mat):
    galaxies = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == '#':
                galaxies.append((i, j))
    return galaxies

def get_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def first_task():
    data = hc.read_file_line('11_2023')
    mat = preprocess_data(data)
    galaxies = get_galaxies(mat)

    sum_of_distances = 0
    for g1 in range(len(galaxies) - 1):
        for g2 in range(g1 + 1, len(galaxies)):
            # print(f'Galaxy {g1} and {g2} have distance {get_distance(galaxies[g1], galaxies[g2])}.')
            sum_of_distances += get_distance(galaxies[g1], galaxies[g2])
    print(sum_of_distances)

def get_distances_expansion(g1, g2, empty_rows, empty_cols, expansion):
    normal_distance = get_distance(g1, g2)
    r1, r2 = g1[0], g2[0]
    r_counter = 0
    for c in empty_rows:
        if r1 < c < r2 or r2 < c < r1:
            r_counter += 1
    c1, c2 = g1[1], g2[1]
    c_counter = 0
    for c in empty_cols:
        if c1 < c < c2 or c2 < c < c1:
            c_counter += 1
    return normal_distance + r_counter * expansion + c_counter * expansion

def second_task():
    data = hc.read_file_line('11_2023')
    galaxies = get_galaxies(data)
    empty_rows = []
    counter = 0
    for line in data:
        if line.count('#') == 0:
            empty_rows.append(counter)
        counter += 1

    empty_cols = []
    counter = 0
    for i in range(len(data[0])):
        column = [line[i] for line in data]
        if column.count('#') == 0:
            empty_cols.append(counter)
        counter += 1
    expansion = 999999
    sum_of_distances = 0
    for g1 in range(len(galaxies) - 1):
        for g2 in range(g1 + 1, len(galaxies)):
            sum_of_distances += get_distances_expansion(galaxies[g1], galaxies[g2], empty_rows, empty_cols, expansion)
            # print(f'Galaxy {g1 + 1} and {g2 +1} have distance {get_distances_expansion(galaxies[g1], galaxies[g2], empty_rows, empty_cols, expansion)}.')
    print(sum_of_distances)

# first_task()
second_task()