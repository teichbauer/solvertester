from TransKlauseEngine import TransKlauseEngine
from bitdic import BitDic
from basics import get_sdic, make_vkdic, perf_count
import pprint
import sys
import time


def initial_bitdic(conf_filename, seed='R'):
    sdic = get_sdic(conf_filename)
    vkdic = make_vkdic(sdic['kdic'], sdic['nov'])
    bitdic = BitDic(seed, seed, vkdic, sdic['nov'])
    return bitdic


def loop_tree(conf_filename, single=False, msg=False, debug=False):
    start_time = time.time()

    root0 = initial_bitdic(conf_filename)
    if debug:
        root0.visualize()
    seed, top_bit = root0.set_txseed()
    tx = TransKlauseEngine(seed, top_bit, root0.vkdic[seed], root0.nov)
    root = tx.trans_bitdic(root0)

    # test_tx(tx, root0.vkdic)

    search_sat(root, single, msg, debug)
    now_time = time.time()
    perf_count['time-used'] = now_time - start_time


def search_sat(root, single, msg, debug):
    nodes = [root]
    while len(nodes) > 0:
        node = nodes.pop(0)
        if debug:
            node.visualize()
        if node.done:
            if msg:
                print(f'{node.name} is done.')
        else:
            if msg:
                print(f'split {node.name}')
            node0, node1 = node.split_topbit(single, debug)
            if node0 == None or node0.done:
                if msg:
                    if node0 == None:
                        bstr = str(node.nov - 1)
                        name = f"{node.name}-{bstr}'0"
                        print(f'{name} is done')
                    else:
                        print(f'{node0.name} is done.')
            else:
                nodes.append(node0)
            if node1 == None or node1.done:
                if msg:
                    if node1 == None:
                        bstr = str(node.nov - 1)
                        name = f"{node.name}-{bstr}'1"
                        print(f'{name} is done')
                    else:
                        print(f'{node1.name} is done.')
            else:
                nodes.append(node1)


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    msg = len(sys.argv) == 3
    debug = len(sys.argv) == 4
    # single = True
    single = False
    if len(sys.argv) == 1:
        config_file_name = 'cfg40-172.json'
        # config_file_name = 'config20_80-9-0.json'
        # config_file_name = 'config1.json'
    else:
        config_file_name = sys.argv[1]
    loop_tree('./configs/' + config_file_name, single, msg, debug)
    nos = len(perf_count['SATS'])
    pp.pprint(perf_count)
    print(f'number of sats: {nos} ')
