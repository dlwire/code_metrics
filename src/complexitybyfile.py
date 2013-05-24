from collections import namedtuple
import re
import sys
from pathgroomer import groom
from parsearguments import parse

class FileComplexity(namedtuple('FileComplexity', ['loc','ccn', 'relative_path'])):
    def __add__(self, rhs):
        return FileComplexity(self.loc + rhs.loc, self.ccn + rhs.ccn, self.relative_path)

    def __str__(self):
        return "%d,%d,%s" % (self.loc, self.ccn, self.relative_path)


def parse_line(line, path=''):
    r = re.compile(r"""^
                    \s*(?P<loc>\d+)
                    \s*(?P<ccn>\d+)
                    \s*(?P<token>\d+)
                    \s*(?P<path>.*)
                    $""", re.X)
    m = r.match(line)
    if m:
        relative_path = groom(m.group('path'), path)
        return FileComplexity(int(m.group('loc')), int(m.group('ccn')), relative_path)
    return None

def accumulate_lines(complexities):
    myMap = {}
    for c in complexities:
        old = myMap.get(c.relative_path, FileComplexity(0,0,''))
        myMap[c.relative_path] = c + old
    return myMap

def process_file(inputData, path=''):
    data = [parse_line(l, path) for l in inputData if l]
    accumulated = accumulate_lines(filter(lambda x: x, data))
   
    return [str(a) for a in accumulated.values()]

if __name__ == '__main__':
    args = parse(sys.argv)
    
    with open(args.data) as f:
        print '\n'.join(process_file(f, args.repo))

