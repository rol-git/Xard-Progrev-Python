def read_lines(path, encoding="utf-8"):
    with open(path, encoding=encoding) as f:
        lines = f.readlines()

    lines = list(filter(lambda x: x, [line.rstrip() for line in lines]))

    return lines
