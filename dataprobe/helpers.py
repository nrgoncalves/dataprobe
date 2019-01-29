def colorize(result):
    color = 'red' if result == 'Violated' else 'Green'
    return 'color: %s' % color


def compute_statistics(columns: list, target_cols: list) -> float:
    '''Compute the number of columns in targetcols that are also present in colums.
    Args:
      columns: fkafa af 
      target_cols: afksaf a

    Return:
      p: proportion of columns in target_cols.
    '''
    p = len(set(columns).intersection(set(target_cols)))
    return p
