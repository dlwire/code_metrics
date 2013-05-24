from xml.etree import ElementTree as ET
from collections import namedtuple
import math
import sys
from pathgroomer import groom
from parsearguments import parse

class FileCoverage(namedtuple('FileCoverage', ['function_count', 'function_coverage', 'branch_count', 'branch_coverage', 'relative_path'])):
    def __str__(self):
        return "%d,%d,%d,%d,%s" % self

def assemble_path(path, name):
    relative_path = name
    if path:
        relative_path = path + '/' + name
    return relative_path
    
def get_ratio(n, d):
    if d == '0':
        return 0
    return  int(math.floor(100 * float(n) / float(d)))

def to_file_coverage(node, path, repo_path=''):
        t = node.attrib
        fn_ratio = get_ratio(t['fn_cov'], t['fn_total'])
        d_ratio = get_ratio(t['d_cov'], t['d_total'])
        relative_path = groom(assemble_path(path, t['name']), repo_path)

        return FileCoverage(int(t['fn_total']), fn_ratio, int(t['d_total']), d_ratio, relative_path)

def process_xml_tree(root, path=None, repo_path=''):
    o = []
    for e in root:
        if 'src' in e.tag:
            o.append(to_file_coverage(e, path, repo_path))
        elif 'folder' in e.tag:
            o += process_xml_tree(e, assemble_path(path, e.attrib['name']), repo_path)
    return o

if __name__ == '__main__':
    args = parse(sys.argv)

    tree = ET.parse(args.data)    
    print '\n'.join(map(str, process_xml_tree(tree.getroot(), repo_path=args.repo)))
