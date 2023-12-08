import helperfunctions as hc
from functools import reduce

def ggt(a, b):
    while b!=0:
        c=a%b
        a=b
        b=c
    return a

def chinese_remainder(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def preprocess_data(data):
    rules = {}
    for line in data:
        splitted = line.split('=')
        source = splitted[0].strip()
        target_splitted = splitted[1].strip().split(',')
        target_left = target_splitted[0][1:]
        target_right = target_splitted[1][:-1]
        rules[source] = (target_left, target_right.strip()) 
    return rules

def first_task():
    data = hc.read_file_line('08_2023')

    directions = data[0]
    data = data[2:]
    rules = preprocess_data(data)
    
    position = 'AAA'
    step_counter = 0
    while position != 'ZZZ':
        rule = rules[position]
        if directions[step_counter % len(directions)] == 'L':
            position = rule[0]
        else:
            position = rule[1]
        step_counter += 1
    print(step_counter)

def find_cycle(rules, directions, position):
    path = []
    step_counter = 0
    finishing_positions_index = []

    start_length = 0
    cycle_length = 0

    cycle = False
    while not cycle:
        path.append(position)
        rule = rules[position]
        if directions[step_counter % len(directions)] == 'L':
            position = rule[0]
        else:
            position = rule[1]
        if position[-1] == 'Z':
            finishing_positions_index.append(len(path))
        step_counter += 1

        for j in range(len(path)):
            if path[j] == position:
                if step_counter % len(directions) == j % len(directions):
                    # found cycle
                    cycle = True
                    start_length = j
                    cycle_length = len(path) - j
                    path.append(position)
                    break
    return path, start_length, cycle_length, finishing_positions_index

def second_task():
    data = hc.read_file_line('08_2023')

    directions = data[0]
    data = data[2:]
    rules = preprocess_data(data)

    positions = [key for key in rules.keys() if key[-1] == 'A']
    cycle_knowledge = []
    max_start_length = 0
    for position in positions:
        print(position)
        _, sl, cl, f= find_cycle(rules, directions, position)
        f_ = [x - sl for x in f if x > sl]
        cycle_knowledge.append([sl, cl, f_])
        if sl > max_start_length:
            max_start_length = sl
    # move all to max_start_length -> inside cycle
    # -> change finishing positions
    for element in cycle_knowledge:
        element[2] = [(x - (max_start_length - element[0])) % element[1] for x in element[2]]
    # now we can use the chinese remainder

    m = [element[1] for element in cycle_knowledge]
    a = [element[2][0] for element in cycle_knowledge]

    # m: [20093, 12169, 13301, 20659, 16697, 17263]
    # a: [20089, 12165, 13297, 20655, 16693, 17259]
    # max start length: 

    print(cycle_knowledge)
    print(m, a)
    print(max_start_length)
    print(chinese_remainder(m, a) + max_start_length)

def clean_for_chinese_remainder(m, a):
    m_new = []
    a_new = []

    done = True
    for i in range(len(m)):
        for j in range(i+1, len(m)):
            g = ggt(m[i], m[j])
            if g == 1:
                m_new.append(m[i])
                a_new.append(a[i])
            elif g == m[i]:
                a2 = m[j] // g
                n2 = m[j] + a[j]

                m_new.append(a2)
                a_new.append(n2 % a2)
            elif g == m[j]:
                a1 = m[i] // g
                n1 = m[i] + a[i]

                m_new.append(a1)
                a_new.append(n1 % a1)
            else:
                done = False
                a1 = m[i] // g
                a2 = m[j] // g

                n1 = m[i] + a[i]
                n2 = m[j] + a[j]

                m_new.append(g)
                if n1 % g != n2 % g:
                    raise ValueError('No solution')
                a_new.append(n1 % g)

                m_new.append(a1)
                m_new.append(a2)

                a_new.append(n1 % a1)
                a_new.append(n2 % a2)

    # m_new.append(m[-1])
    # a_new.append(a[-1])
    # remove duplicates in m_new
    removing_indizes = set()
    for i in range(len(m_new)):
        for j in range(i+1, len(m_new)):
            if m_new[i] == m_new[j]:
                removing_indizes.add(j)
    removing_indizes = list(removing_indizes)
    removing_indizes.sort(reverse=True)
    for i in removing_indizes:
        del m_new[i]
        del a_new[i]
    print(f'old: {m}, {a}')
    print(f'new: {m_new}, {a_new}')
    print(f'removing {removing_indizes}')
    if not done:
        return clean_for_chinese_remainder(m_new, a_new)
    return m_new, a_new


# first_task()
# second_task()

# m = [3, 4, 7]
# a = [1, 1, 0]

# m = [2, 6, 9]
# a = [0, 2, 2]
# print(clean_for_chinese_remainder(m, a))
# print(chinese_remainder(m, a))

# print(ggt(5, 35))

max_length = 4
m = [20093, 12169, 13301, 20659, 16697, 17263]
for i in range(len(m)):
    for j in range(i+1, len(m)):
        print(f'ggt({m[i]}, {m[j]}) = {ggt(m[i], m[j])}')

for i in range(len(m)):
    print(m[i] // 283)

a = [20089, 12165, 13297, 20655, 16693, 17259]
m_new = [71, 43, 47, 73, 59, 61, 283]
a_new = []
for i in range(len(m)):
    a_new.append((a[i] + m[i]) % m_new[i])
a_new.append((a[0] + m[0]) % m_new[-1])

# too low: 10668805667827
print(chinese_remainder(m_new, a_new) + max_length)
