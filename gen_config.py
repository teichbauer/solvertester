import sys
from cnfgenerator import Generator
from cnf2config import readfile, make_sdic, verify_and_make_config


def gen(nov, nok):
    pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("python gen_config.py <nov> <nok>")
        nov = 12
        nok = 40
    else:
        nov = int(sys.argv[1])
        nok = int(sys.argv[2])
    g = Generator(nov, nok)
    out_cnf_filename = f'cnf{nov}-{nok}.cnf'
    out_cfg_file = f'cfg{nov}-{nok}.json'
    g.generate(out_cnf_filename)
    nv, nk, clines = readfile(out_cnf_filename)
    sdic = make_sdic(nv, clines)
    verify_and_make_config(sdic, out_cfg_file)
