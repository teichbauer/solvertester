import sys
from cnfgenerator import Generator
from cnf2config import readfile, make_sdic, verify_and_make_config


def gen(nov, nok):
    pass


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("python gen_config.py <nov> <nok> <cnf-file-name>")
        nov = 12
        nok = 40
        file_name = 'test-config.json'
    else:
        nov = int(sys.argv[1])
        nok = int(sys.argv[2])
        file_name = sys.argv[3]
    g = Generator(nov, nok)
    filename = f'cnf{nov}-{nok}.cnf'
    g.generate(filename)
    nv, nk, clines = readfile(filename)
    sdic = make_sdic(nv, clines)
    verify_and_make_config(sdic, file_name)
