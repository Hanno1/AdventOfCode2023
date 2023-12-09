import helperfunctions as hc

def preprocess_data(data):
    mat = []
    for line in data:
        mat.append([int(i) for i in line.split(" ")])
    return mat

def compute_distance(list_):
    new_list = []
    for i in range(len(list_) - 1):
        new_list.append(list_[i + 1] - list_[i])
    return new_list

def first_task():
    data = hc.read_file_line("09_2023")
    mat = preprocess_data(data)
    sum_ = 0
    for line in mat:
        # get first line with distance 0
        all_distances = [line]
        distances = line
        done = False
        while not done:
            distances = compute_distance(distances)
            all_distances.append(distances)

            done = True
            for d in distances:
                if d != 0:
                    done = False
                    break
        # compute it back
        all_distances = all_distances[::-1]
        all_distances[0].append(0)
        for i in range(1, len(all_distances)):
            new_val = all_distances[i - 1][-1] + all_distances[i][-1]
            all_distances[i].append(new_val)
        sum_ += all_distances[-1][-1]
    # 2105961943
    print(sum_)

def second_task():
    data = hc.read_file_line("09_2023")
    mat = preprocess_data(data)
    sum_ = 0
    for line in mat:
        # get first line with distance 0
        all_distances = [line]
        distances = line
        done = False
        while not done:
            distances = compute_distance(distances)
            all_distances.append(distances)

            done = True
            for d in distances:
                if d != 0:
                    done = False
                    break
        # compute it back
        all_distances = all_distances[::-1]
        all_distances[0].insert(0, 0)
        for i in range(1, len(all_distances)):
            new_val = all_distances[i][0] - all_distances[i - 1][0]
            all_distances[i].insert(0, new_val)
        # print(all_distances)
        sum_ += all_distances[-1][0]
    print(sum_)

# first_task()
second_task()   
