characters = ' '.join('abcdefghijklmnopqrstuvwxyz').split()
characters += ' '.join('ABCDEFGHIJKLMNOPQRSTUVWXYZ').split()

def cull_colors(string):
    for c in characters:
        string = string.replace("|%s" % c, "")

    return string
