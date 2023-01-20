from math import ceil
from itertools import chain, combinations
from copy import deepcopy

def sublist(lst1, lst2):
    from collections import Counter
    c1 = Counter(lst1)
    c2 = Counter(lst2)
    for item, count in c1.items():
        if count > c2[item]:
            return False
    return True

def transponder_set(demand):
    transponders = [100, 200, 400]
    # znalezienie minimalnej liczby minimalnych transponderów która zaspokoi zapotrzebowanie
    tr_num = ceil(demand/min(transponders))
    transponders = tr_num*transponders
    transponders_subsets = list(chain.from_iterable(combinations(transponders, r) for r in range(len(transponders)+1)))[1:]
    for i in range(len(transponders_subsets)):
        transponders_subsets[i] = list(transponders_subsets[i])
        transponders_subsets[i].sort()
    res = []
    [res.append(x) for x in transponders_subsets if x not in res]
    transponders_subsets = res
    transponders_set = []
    temp_transponders_subsets = deepcopy(transponders_subsets)
        
    for i in range(len(transponders_subsets)):
        try:
            subset = transponders_subsets[i]
            if sum(subset) >= demand:
                transponders_set.append(subset)
                for inner_subset in transponders_subsets:
                    if sublist(subset, inner_subset):
                        if subset != inner_subset:
                            try:
                                temp_transponders_subsets.remove(inner_subset)
                            except:
                                pass
            else:
                try:
                    temp_transponders_subsets.remove(subset)
                except:
                    pass
        except:
            break
    return(temp_transponders_subsets)

if __name__ == '__main__':
    print(transponder_set(320))