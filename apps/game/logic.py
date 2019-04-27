import random


directions = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


def handle_field_test(field, x, y, size):
    mark, visible, _ = field[x][y]

    if mark != ' ' or visible:  # digit or already passed
        # display it and return
        field[x][y][1] = True
        return

    field[x][y][1] = True  # show empty field

    for direction in directions:
        dx = x + direction[0]
        dy = y + direction[1]

        if dx < 0 or dy < 0 or dx >= size or dy >= size:
            continue

        handle_field_test(field, dx, dy, size)


def handle_game_lose(field, size):
    """
    Disclose all mines
    """
    for i in range(size):
        for g in range(size):
            if field[i][g][0] == '*':
                field[i][g][1] = True


def check_game_win(field, size):
    """
    win = all fiels are flagged or only mine fields is left on field
    """
    for i in range(size):
        for g in range(size):
            mark, visible, flagged = field[i][g]
            if visible or flagged:
                continue

            if mark != '*':
                return False

    return True


def generate_field(size, mines_count):
    # 1: generate random mines array
    mines_array = ['*'] * mines_count + [' '] * (size * size - mines_count)
    random.shuffle(mines_array)

    # 2: make matrix
    field = []
    for i in range(size):
        field.append(mines_array[i*size:i*size+size])

    # 3: fill matrix with digits
    for i in range(size):
        for g in range(size):
            if field[i][g] != '*':
                mines_count = _nearby_mines_count(field, i, g, size)
                if mines_count > 0:
                    field[i][g] = mines_count

    # 4: build result field
    result = []
    for i in range(size):
        result.append([])
        for g in range(size):
            result[i].append([])
            result[i][g] = [field[i][g], False, False]

    return result


def _nearby_mines_count(field, x, y, size):
    result = 0

    for direction in directions:
        dx = x + direction[0]
        dy = y + direction[1]

        if dx < 0 or dy < 0 or dx >= size or dy >= size:
            continue

        if field[dx][dy] == '*':
            result += 1

    return result
