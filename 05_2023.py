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
    resulting_seeds = []
    rest_seeds = []
    for dest_m, source_m, range_m in mapping:
        # 4 possibilities:
        # 1) start seed in range
        if source_m <= start_seed < source_m + range_m:
            # 1.1) range in range as well, no rest seeds
            if start_seed + range_ <= source_m + range_m:
                resulting_seeds.append([dest_m + (start_seed - source_m), range_])
            # 1.2) range is not in range
            else:
                rest_startseed = source_m + range_ + 1
                rest_range = range_ - (rest_startseed - start_seed)

                print(rest_startseed, rest_range)

                resulting_seeds.append([dest_m + (start_seed - source_m), (rest_startseed - start_seed)])
                res, rest = map_with_range([rest_startseed, rest_range], mapping)
                resulting_seeds.append(res)
                rest_seeds.append(rest)
        # 2) start seed not in range -> start seed bigger
        elif start_seed >= source_m + range_m:
            resulting_seeds.append([dest_m + range_m, range_])
            
    if rest_seeds != []:
        resulting_seeds += rest_seeds
    return resulting_seeds, rest_seeds

def second_task():
    data = hc.read_file_line("05_2023")
    mat = preprocess_data(data)
    lowest_loc = math.inf
    for entry in range(0, len(mat[0]), 2):
        seed = mat[0][entry]
        range_ = mat[0][entry + 1]
        actual_seeds = [[seed, range_]]
        for act_seed in actual_seeds:
            pass
    print(lowest_loc)

# first_task()
# second_task()

seed = [2, 4]
mapping = [[1, 0, 5]]
print(map_with_range(seed, mapping))
    