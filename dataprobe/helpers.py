from functools import reduce


def colorize(result):
    color = 'red' if result == 'Violated' else 'Green'
    return 'color: %s' % color


def flatten_list(x_any: list) -> list:
    '''Flatten a list to a maximum of one nested level,'''
    if x_any == []:
        return []

    x_list = list(map(lambda x: [x] if type(x) != list else x, x_any))
    if x_list == []:
        return []

    x_flat = reduce(lambda x, y: x + y, x_list)
    return list(x_flat)


def compute_statistics(columns: list, target_cols: list) -> float:
    raise NotImplementedError
