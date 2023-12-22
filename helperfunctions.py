def read_file(filename):
    with open(f'inputs/{filename}.txt') as f:
        content = f.read()
    return content

def read_file_line(filename):
    lines = []
    with open(f'inputs/{filename}.txt') as f:
        for line in f.readlines():
            lines.append(line.replace('\n', ''))
    return lines

def sort_vertical_lines(lines):
    # minimum x value first
    lines.sort(key=lambda line: line[0][0])
    for line in lines:
        if line[0][1] > line[1][1]:
            line[0], line[1] = line[1], line[0]
    return lines

def sort_horizontal_lines(lines):
    # minimum x value first
    for line in lines:
        if line[0][0] > line[1][0]:
            line[0], line[1] = line[1], line[0]
    lines.sort(key=lambda line: line[0][0])
    return lines

def get_area(lines):
    # lines have form -> [(x,y), (x,y)]
    # first there are horizontal lines and then vertical lines
    #       [[[(x,y), (x,y)]], [[(x,y), (x,y)], [(x,y), (x,y)]]]
    # only take y values
    # min y is in a vertical line, so is max y as well as x
    horizontal_lines = lines[0]
    vertical_lines = lines[1]

    min_y = vertical_lines[0][0][1]
    max_y = vertical_lines[0][0][1]
    min_x = vertical_lines[0][0][0]
    max_x = vertical_lines[0][0][0]

    for line in vertical_lines:
        end_1 = line[0]
        end_2 = line[1]
        for entry in [end_1, end_2]:
            if entry[1] < min_y:
                min_y = entry[1]
            if entry[1] > max_y:
                max_y = entry[1]
            if entry[0] < min_x:
                min_x = entry[0]
            if entry[0] > max_x:
                max_x = entry[0]

    area = 0
    # start with top row and go to the lowest row

    hor_lines_dict = {}
    for line in horizontal_lines:
        if line[0][1] not in hor_lines_dict:
            hor_lines_dict[line[0][1]] = [line]
        else:
            hor_lines_dict[line[0][1]].append(line)

    last_area = 0
    last_not_hor = False
    for y in range(min_y, max_y + 1):
        inside = False
        last_vert_dir = None
        # current_horizontal_lines = [line for line in horizontal_lines if 
        #                             line[0][1] == y]
        current_horizontal_lines = hor_lines_dict[y] if y in hor_lines_dict else []
        current_horizontal_lines = sort_horizontal_lines(current_horizontal_lines)

        if last_not_hor and len(current_horizontal_lines) == 0:
            area += last_area
            continue  
        
        if len(current_horizontal_lines) == 0:
            last_not_hor = True
        else:
            last_not_hor = False

        current_vertical_lines = [line for line in vertical_lines if 
                                  (line[0][1] <= y and line[1][1] >= y) or 
                                  (line[0][1] >= y and line[1][1] <= y)]
        current_vertical_lines = sort_vertical_lines(current_vertical_lines)
        
        # sort vertical lines by x value
        last_area = 0
        hor_line_pos = 0
        # start with first vertical line

        # print(y, current_vertical_lines, current_horizontal_lines)
        last_hor_line = False
        for vert_line_pos in range(len(current_vertical_lines)):
            # either new horziontal line or no horizontal line
            # horizontal line
            inside = not inside
            area += 1
            last_area += 1

            if hor_line_pos < len(current_horizontal_lines):
                horizontal_line = current_horizontal_lines[hor_line_pos]
            else:
                last_hor_line = True
            vertical_line = current_vertical_lines[vert_line_pos]
            if horizontal_line[0][0] == vertical_line[0][0] and not last_hor_line:
                # horizontal line starts here
                dif = horizontal_line[1][0] - horizontal_line[0][0] - 1
                area += dif
                last_area += dif

                # get direction
                current_end = vertical_line[1][1] if vertical_line[1][1] == y else vertical_line[0][1]
                other_end = vertical_line[0][1] if vertical_line[1][1] == y else vertical_line[1][1]
                last_vert_dir = 'up' if current_end < other_end else 'down'
            elif horizontal_line[1][0] == vertical_line[0][0] and not last_hor_line:
                # horizontal line ends here
                hor_line_pos += 1
                # check if inside or outside

                current_end = vertical_line[1][1] if vertical_line[1][1] == y else vertical_line[0][1]
                other_end = vertical_line[0][1] if vertical_line[1][1] == y else vertical_line[1][1]
                current_vertical_direction = 'up' if current_end < other_end else 'down'
                if last_vert_dir != current_vertical_direction:
                    # area -= 1
                    # last_area -= 1
                    inside = not inside
                if inside:
                    # print('inside1')
                    next_vert_line = current_vertical_lines[vert_line_pos + 1]
                    dif = next_vert_line[0][0] - vertical_line[0][0] - 1
                    area += dif 
                    last_area += dif
            # no horizontal line
            else:
                if inside:
                    # print("inside")
                    next_vert_line = current_vertical_lines[vert_line_pos + 1]
                    dif = next_vert_line[0][0] - vertical_line[0][0] - 1
                    area += dif 
                    last_area += dif
        # print(y, last_area)
    return area


if __name__ == '__main__':
    hor_lines = [[(0, 0), (2, 0)], [(0, 2), (1, 2)], [(1, 1), (2, 1)]]
    vert_lines = [[(0, 0), (0, 2)], [(2, 0), (2, 1)], [(1, 1), (1, 2)]]

    ar = get_area([hor_lines, vert_lines])
    print(ar)
