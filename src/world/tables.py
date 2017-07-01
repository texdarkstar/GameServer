attributes = {
    0: -2,
    1: -2,
    2: -2,
    3: -1,
    4: -1,
    5: -1,
    6: 0,
    7: 0,
    8: 0,
    9: 1,
    10: 1,
    11: 1,
    12: 2,
    13: 2,
    14: 2,
    15: 3,
}


def dm_attr(attr):
    if attr > 15:
        attr = 15

    elif attr < 0:
        attr = 0

    print str(attr) + ": " + str(attributes[attr])

    return attributes[attr]
