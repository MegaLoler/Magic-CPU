def combinations(ls):
    ''' return a list of combinations of items in lists

    ls = list of lists
    return a list that is all possible combinations of each item in each list
    
    for example:
    combinations((1,2),(3,4),(5,6)) => ((1,3,5),(1,3,6),(1,4,5),(1,4,6),(2,3,5),(2,3,6),(2,4,5),(2,4,6))
    '''
    # this is ugly lol
    # rather rewrite it functionally? recursively? that'd be cool
    # but it was making my head spin so
    if len(ls) == 0: return ls
    indices = [0]*len(ls)
    combos = list()
    for i in ls:
        if len(i) == 0: return combos
    while True:
        combo = list()
        for i in range(len(ls)):
            index = indices[i]
            combo.append(ls[i][index])
        combos.append(combo)
        i = len(ls)-1
        while True:
            indices[i] += 1
            if indices[i] == len(ls[i]):
                indices[i] = 0
                i -= 1
                if i == -1: return combos
            else: break
