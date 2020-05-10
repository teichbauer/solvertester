from vklause import VKlause
from basics import make_vkdic
import sys


def verify(vkdic, v):
    verified = True
    for kname, vk in vkdic.items():
        if vk.hit(v):
            verified = False
            print(f'Failed on {kname}')
    if verified:
        print(f'{v} is verified to satisfy all.')
    else:
        print(f'{v} does not satify.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'python verifysat.py <conf-file-name> <value>')
        config_file_name = 'config8_38.json'
        value = 130  # 2 130 146 150
    else:
        config_file_name = sys.argv[1]
        value = int(sys.argv[2])
    da = open(f'configs/'+config_file_name).read()
    sdic = eval(da)
    vkdic = make_vkdic(sdic['kdic'], sdic['nov'])
    verify(vkdic, value)
