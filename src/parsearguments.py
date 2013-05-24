import argparse

def parse(args):
    p = argparse.ArgumentParser(description='Parse data file and repo location')
    p.add_argument('--data', required=True, help='location of the data to parse')
    p.add_argument('--repo', required=False, default='', help='repo root to be stripped off file locations in output')

    return p.parse_args(args[1:])
