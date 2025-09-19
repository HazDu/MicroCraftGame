import random
import __main__ as main


def generate_tree(queue, chunk):
    for coords in queue:
        if 0 < coords[0] - 2 < coords[0] + 2 < 64 and 0 < coords[1] - 4:
            chunk[coords[0]][coords[1]] = int(10)
            chunk[coords[0]][coords[1] - 1] = int(10)
            chunk[coords[0]][coords[1] - 2] = int(10)
            chunk[coords[0]][coords[1] - 3] = int(10)
            chunk[coords[0]][coords[1] - 4] = int(11)
            chunk[coords[0] - 1][coords[1] - 2] = int(11)
            chunk[coords[0] - 1][coords[1] - 3] = int(11)
            chunk[coords[0] - 1][coords[1] - 4] = int(11)
            chunk[coords[0] + 1][coords[1] - 2] = int(11)
            chunk[coords[0] + 1][coords[1] - 3] = int(11)
            chunk[coords[0] + 1][coords[1] - 4] = int(11)
            chunk[coords[0] + 2][coords[1] - 2] = int(11)
            chunk[coords[0] + 2][coords[1] - 3] = int(11)
            chunk[coords[0] - 2][coords[1] - 2] = int(11)
            chunk[coords[0] - 2][coords[1] - 3] = int(11)
    return chunk

def generate_chunk():
    contents = []
    tree_queue = []
    for y in range(64):
        row = []
        for x in range(64):
            if random.randint(0, 100) == 0:
                tree_queue.append((x, y))
            row.append(random.randint(2, 2))
        contents.append(row)
    contents = generate_tree(tree_queue, contents)
    return contents #[[random.randint(2, 2) for _ in range(64)] for _ in range(64)]