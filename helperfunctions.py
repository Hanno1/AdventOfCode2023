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
