import helperfunctions as hc
import math

# NAMES = ['soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']

def preprocess_data(data):
    mat = []
    content = []
    # append seeds:
    line = data[0]
    l = line.split(':')[1].split(' ')
    l.remove('')
    mat.append([int(entry) for entry in l])

    for line in data:
        if line == '':
            if content != []:
                mat.append(content)
                content = []
            continue
        if line[0].isdigit():
            l = line.split(' ')
            content.append([int(entry) for entry in l])
    mat.append(content)
    return mat

def map(entry, mapping):
    for dest, source, range_ in mapping:
        if source <= entry < source + range_:
            return dest + (entry - source)
    return entry

def first_task():
    data = hc.read_file_line("05_2023")
    mat = preprocess_data(data)
    seeds = mat[0]
    # results = []
    lowest_loc = math.inf
    for seed in seeds:
        current_seed = seed
        for i in range(1, len(mat)):
            current_seed = map(current_seed, mat[i])
        # results.append(current_seed)
        if current_seed < lowest_loc:
            lowest_loc = current_seed
    print(lowest_loc)

def map_with_range(entry, mapping):
    start_seed, range_ = entry
    final_seed = start_seed + range_ - 1
    for dest_m, source_m, range_m in mapping:
        final_m = source_m + range_m - 1
        # 4 possibilities:
        # 1) start seed in range
        if source_m <= start_seed < source_m + range_m:
            # 1.1) range in range as well, no rest seeds
            if start_seed + range_ <= source_m + range_m:
                return [[dest_m + (start_seed - source_m), range_]]
            # 1.2) range is not in range
            else:
                rest_startseed = final_m + 1
                rest_range = final_seed - final_m
                res = map_with_range([rest_startseed, rest_range], mapping)

                return [[dest_m + (start_seed - source_m), final_m - start_seed + 1]] + res
        # 2) start seed not in range but final seed is in range:
        elif source_m <= final_seed <= final_m:
            rest_range = source_m - start_seed
            res = map_with_range([start_seed, rest_range], mapping)

            return [[dest_m, final_seed - source_m + 1]] + res

        # 3) start seed not in range and final seed not in range, but middle in range:
        elif start_seed < source_m and final_m < final_seed:
            first_range = source_m - start_seed
            second_range = final_seed - final_m

            res1 = map_with_range([start_seed, first_range], mapping)
            res2 = map_with_range([final_m + 1, second_range], mapping)

            return [[dest_m, range_m]] + res1 + res2
    return [entry]

def second_task():
    data = hc.read_file_line("05_2023")
    mat = preprocess_data(data)
    lowest_loc = math.inf
    for entry in range(0, len(mat[0]), 2):
        seed = mat[0][entry]
        range_ = mat[0][entry + 1]
        actual_seeds = [[seed, range_]]
        for i in range(1, len(mat)):
            next_seeds = []
            for j in range(len(actual_seeds)):
                next_seeds += map_with_range(actual_seeds[j], mat[i])
            actual_seeds = next_seeds
        # print(actual_seeds)
        for seed_c, _ in actual_seeds:
            if seed_c < lowest_loc:
                lowest_loc = seed_c
    # 260990830 - too high
    print(lowest_loc)

# first_task()
second_task()

# seed = [9, 10]
# mapping = [[11, 10, 10]]
# print(map_with_range(seed, mapping))
    