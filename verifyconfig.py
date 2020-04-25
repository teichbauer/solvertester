import sys


def verify(kdic, nov):
    knames = list(kdic.keys())
    while len(knames) > 0:
        kn0 = knames.pop(0)
        k0 = kdic[kn0]
        hb0 = sorted(list(k0.keys()))[-1]
        if hb0 >= nov:
            return False, None, None
        for kn in knames:
            k = kdic[kn]
            hb = sorted(list(k.keys()))[-1]
            if hb >= nov:
                return False, kn, None
            if k == k0:
                return False, kn, kn0
    return True, None, kn0


if __name__ == '__main__':
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        fname = 'config1.json'
    sdic = eval(open('./configs/' + fname).read())
    res, kn, kn0 = verify(sdic['kdic'], sdic['nov'])
    if res:
        print(f'{fname} is ok')
    else:
        if kn0 == None:
            nov = sdic['nov']
            print(f'bit number higher than {nov}')
        else:
            print(f'{kn} and {kn0} are duplicates')
