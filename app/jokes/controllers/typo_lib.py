import math

def insertion_cost(mes, j):
    return 1


def deletion_cost(mes, j):
    return 1


adj_chars = [('a', 'q'), ('a', 's'), ('a', 'z'), ('b', 'g'), ('b', 'm'),
             ('b', 'n'), ('b', 'v'), ('c', 'd'),
             ('c', 'v'), ('c', 'x'), ('d', 'c'), ('d', 'e'), ('d',
                                                              'f'),
             ('d', 's'), ('e', 'd'), ('e', 'r'),
             ('e', 'w'), ('f', 'd'), ('f', 'g'), ('f', 'r'), ('f',
                                                              'v'),
             ('g', 'b'), ('g', 'f'), ('g', 'h'),
             ('g', 't'), ('h', 'g'), ('h', 'j'), ('h', 'm'), ('h',
                                                              'n'),
             ('h', 'y'), ('i', 'k'), ('i', 'o'),
             ('i', 'u'), ('j', 'h'), ('j', 'k'), ('j', 'u'), ('k',
                                                              'i'),
             ('k', 'j'), ('k', 'l'), ('l', 'k'),
             ('l', 'o'), ('m', 'b'), ('m', 'h'), ('n', 'b'), ('n',
                                                              'h'),
             ('o', 'i'), ('o', 'l'), ('o', 'p'),
             ('p', 'o'), ('q', 'a'), ('q', 'w'), ('r', 'e'), ('r',
                                                              'f'),
             ('r', 't'), ('s', 'a'), ('s', 'd'),
             ('s', 'w'), ('s', 'x'), ('t', 'g'), ('t', 'r'), ('t',
                                                              'y'),
             ('u', 'i'), ('u', 'j'), ('u', 'y'),
             ('v', 'b'), ('v', 'c'), ('v', 'f'), ('w', 'e'), ('w',
                                                              'q'),
             ('w', 's'), ('x', 'c'), ('x', 's'),
             ('x', 'z'), ('y', 'h'), ('y', 't'), ('y', 'u'), ('z', 'a'), ('z', 'x')]


def subst_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    elif (query[i-1], message[j-1]) in adj_chars:
        return 1.75
    else:
        return 2


def edit_matrix(query, message, thresh):
    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m):
        chart[i, 0] = chart[i-1, 0] + insertion_cost(query, i)
    for j in range(1, n):
        chart[0, j] = chart[0, j-1] + deletion_cost(message, j)
    for i in range(1, m):
        exceeded_max = True
        for j in range(1, n):
            chart[i, j] = min(
                chart[i-1, j] + deletion_cost(query, i),
                chart[i, j-1] + insertion_cost(message, j),
                chart[i-1, j-1] + subst_cost(query, message, i, j)
            )
            # NEW : Check to see if any are below the thresh
            exceeded_max = exceeded_max and (chart[i, j] >= thresh)
        # NEW : exceeded_max means already not the minimum edit_distance, won't be the typo
        if exceeded_max: # NEW : this means all exceeded the maximum
            chart[len(query), len(message)] = thresh + 1 # NEW : set it to above the maximum
            return chart
    return chart


def edit_distance(query, message, thresh):
    query = query.lower()
    message = message.lower()

    matrix = edit_matrix(query, message, thresh)
    return matrix[(len(query), len(message))]


def closest_word(query, alt_opts):
    """
    Returns a tuple (res, dist) where res is the closest word query is to in 
    alt_opts and dist is the edit distance. 
    """
    result = []
    curr_min = math.inf # NEW: Keep track of the miniumum edit distance
    for i in range(len(alt_opts)):
        if abs(len(query) - len(alt_opts[i])) <= 3:
            dist = edit_distance(query, alt_opts[i], curr_min)
            if dist < curr_min:
                curr_min = dist
            result.append((alt_opts[i], dist))
    result.sort(key=lambda t: t[1])
    if result: 
        return result[0]
    else: 
        return None
