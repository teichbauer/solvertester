import sys
from bitgroup import BitGroup
from basics import get_sdic, make_vkdic


def merge_sat_tuple(t, hnov):
    shft = hnov - 1
    t0, t1 = t
    res = (t0 << shft) + 1
    return res


def merge_sat_tuples(ts, hnov):
    lst = []
    for t in ts:
        lst.append(merge_sat_tuple(t, hnov))
    return lst


if __name__ == '__main__':
    if len(sys.argv) == 2:
        cfg_file = sys.argv[1]
    else:
        cfg_file = 'cfg6-13.json'
    sdic = get_sdic('./configs/' + cfg_file)
    nov = sdic['nov']
    vkdic = make_vkdic(sdic['kdic'], nov)
    bg = BitGroup('group', vkdic, sdic['nov'])
    sats = bg.solve()
    satlst = merge_sat_tuples(sats, nov // 2)
    print(f'sats: {sats}, or ')
    print(f'{satlst}')
