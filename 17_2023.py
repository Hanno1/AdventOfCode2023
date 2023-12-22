import helperfunctions as hc
import math

def preprocess(data):
    return [[int(x) for x in line] for line in data]

def explore_one_step(mat, x, y, direction, heat, steps):
    new_positions = []
    val = 4
    # go up
    if x > 0 and direction != 'down':
        if direction == 'up':
            if steps + 1 < val:
                new_positions.append([(x - 1, y), 'up', heat + mat[x - 1][y], steps + 1])
        else:
            new_positions.append([(x - 1, y), 'up', heat + mat[x - 1][y], 1])

    # go down
    if x < len(mat) - 1 and direction != 'up':
        if direction == 'down':
            if steps + 1 < val:
                new_positions.append([(x + 1, y), 'down', heat + mat[x + 1][y], steps + 1])
        else:
            new_positions.append([(x + 1, y), 'down', heat + mat[x + 1][y], 1])

    # go right
    if y < len(mat[0]) - 1 and direction != 'left':
        if direction == 'right':
            if steps + 1 < val:
                new_positions.append([(x, y + 1), 'right', heat + mat[x][y + 1], steps + 1])
        else:
            new_positions.append([(x, y + 1), 'right', heat + mat[x][y + 1], 1])

    # go left
    if y > 0 and direction != 'right':
        if direction == 'left':
            if steps + 1 < val:
                new_positions.append([(x, y - 1), 'left', heat + mat[x][y - 1], steps + 1])
        else:
            new_positions.append([(x, y - 1), 'left', heat + mat[x][y - 1], 1])

    return new_positions

def explore(mat):
    start = (0, 0)
    # (position, direction, heat, steps in one direction)
    current_heads = [[start, 'right', 0, 0]]
    visited = []
    visited_heats = []

    min_heat = math.inf
    counter = 0
    max_steps = len(mat) * len(mat[0])
    end = (len(mat) - 1, len(mat[0]) - 1)
    while current_heads:
        print(counter)
        new_heads = []
        # print(current_heads)
        if counter > max_steps:
            break
        for head in current_heads:
            x, y = head[0]
            direction = head[1]
            if x == end[0] and y == end[1]:
                if head[2] < min_heat:
                    min_heat = head[2]
                    print(min_heat)
                continue
            if (x, y, direction) in visited:
                index = visited.index((x, y, direction))
                if head[2] < visited_heats[index]:
                    visited_heats[index] = head[2]
                else:
                    continue
            new_heads += explore_one_step(mat, x, y, direction, head[2], head[3])
            visited.append((x, y, direction))
            visited_heats.append(head[2])
        current_heads = new_heads
        counter += 1
    print(min_heat)
    return min_heat

def first_task():
    data = preprocess(hc.read_file_line("17_2023"))
    result = explore(data)
    # print(result)

first_task()