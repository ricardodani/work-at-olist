def in_range(range, obj):
    '''Test if `obj` is in a `range` tuple.
    '''
    start, end = range
    return start >= obj > end
