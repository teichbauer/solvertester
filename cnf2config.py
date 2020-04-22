# -----------------------------------------------------------------------------
#  convert a cnf file from under ./data/* to a <fn>.json file with all clauses
# in the following format.
# The example has  <number of variables> = 8, <number of clauses>: 38
# {
#    "nov": <>,
#    "kdic": {
#       "C0001": {7: 0, 5: 1, 0: 0},  # highst bit: 7,set to 1, bit-0 set to 0
#       "C0002": {...},
#       ...
#       "C0038": {...}
#    }
# }
# ============================================================================


import sys


def readfile(file_name):
    fil = open('data/' + file_name)
    lines = fil.readlines()
    nov = -1
    nok = -1
    clines = []
    for line in lines:
        if line.startswith('c'):
            continue
        elif line.startswith('p'):
            splt = line.split()
            nov = int(splt[2])
            nok = int(splt[-1])
        else:
            if line.startswith('%'):
                break
            splt = line.split()
            clines.append(tuple(splt[:3]))
    return nov, nok, clines


def print2file(sdic, filename):
    from pprint import pprint
    with open(filename, 'wt') as out:
        pprint(sdic, stream=out)


def make_sdic(nov, cls):
    kcount = 0
    sdic = {"nov": nov, "kdic": {}}
    for tup in cls:
        kcount += 1
        kname = 'C' + str(kcount).zfill(4)
        dic = {}
        for t in tup:
            i = int(t)
            bit = abs(i) - 1
            if i < 0:
                dic[bit] = 1
            else:
                dic[bit] = 0
        sdic["kdic"][kname] = dic
    return sdic


if __name__ == '__main__':
    fname = sys.argv[1]
    nv, nk, clines = readfile(fname)
    sdic = make_sdic(nv, clines)
    print2file(sdic, './configs/config.json')
