import re

def groom(path, prefix=''):
    if not prefix == '':
        prefix += '/*'
    r = re.compile('^' + prefix + "(.*)")
    m = r.match(path)

    if m: 
        return m.group(1)
    else:
        return path
