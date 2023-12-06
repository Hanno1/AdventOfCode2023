import helperfunctions as hc

def preprocess_data(data):
    first_row = data[0].split(':')[1].strip()
    first_row = first_row.split(' ')
    times = [int(entry) for entry in first_row if entry != '']
    second_row = data[1].split(':')[1].strip()
    second_row = second_row.split(' ')
    distances = [int(entry) for entry in second_row if entry != '']
    return times, distances

def first_task():
    data = hc.read_file_line("06_2023")
    times, distances = preprocess_data(data)
    prod = 1
    for race in range(len(times)):
        time, dist = times[race], distances[race]
        possibilities = 0
        # charge the boat:
        for charging_time in range(1, time):
            traveled_dist = charging_time * (time - charging_time)
            if traveled_dist > dist:
                possibilities += 1
            elif possibilities > 0:
                break
        prod *= possibilities
    print(prod)

def second_task():
    data = hc.read_file_line("06_2023")
    times, distances = preprocess_data(data)
    time = ''.join([str(t) for t in times])
    dist = ''.join([str(d) for d in distances])

    first_poss = 0
    second_poss = 0

    # implement binary search
    def test_possible(charging_time):
        traveled_dist = charging_time * (int(time) - charging_time)
        if traveled_dist > int(dist):
            return True
        return False
    
    def binary_search(start, end):
        if start == end:
            return start
        mid = (start + end) // 2
        if test_possible(mid):
            return binary_search(start, mid)
        else:
            return binary_search(mid + 1, end)
        
    def r_binary_search(start, end):
        if start == end:
            return start - 1
        mid = (start + end) // 2
        if test_possible(mid):
            return r_binary_search(mid + 1, end)
        else:
            return r_binary_search(start, mid)
        
    first = binary_search(1, int(time) // 2)
    second = r_binary_search(int(time) // 2, int(time))

    print(first, second)
    print(second - first + 1)

# first_task()
second_task()