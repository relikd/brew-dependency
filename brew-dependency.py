#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import json

ARGS = None


def main():
    global ARGS
    parser = ArgumentParser()
    parser.add_argument('filter', nargs='*', help='matches same beginning')
    parser.add_argument('-a', '--all', action='store_true',
                        help='show subdependencies toplevel')
    parser.add_argument('-r', '--reverse', action='store_true',
                        help='print dependants instead')
    ARGS = parser.parse_args()

    A = parseCellar('/usr/local/Cellar/', 'INSTALL_RECEIPT.json')
    B = generateTree(A)
    printReverse(A, B) if ARGS.reverse else printNormal(A, B)


def iterDirs(base):
    for d in os.listdir(base):
        x = os.path.join(base, d)
        if os.path.isdir(x):
            yield x


def parseCellar(root, cfg):
    list = {}
    apps = [os.path.join(y, cfg) for x in iterDirs(root) for y in iterDirs(x)]
    for config in apps:
        with open(config, 'r') as f:
            j = json.load(f)
            src = j['source']
            name = os.path.split(src['path'])[1][:-3]
            version = src['versions'][src['spec']]
            flags = (j['installed_on_request'], j['installed_as_dependency'])
            list[name] = {'v': version, 'f': flags, 'u': False, 'd': []}

            for rd in j['runtime_dependencies']:
                list[name]['d'].append([rd['full_name'], rd['version']])
    return list


def recurDeps(parent, children, master):
    for name, version in children:
        parent[name] = {'!': version}
        recurDeps(parent[name], master[name]['d'], master)
        master[name]['u'] = True


def generateTree(master):
    list = {}
    for name, val in master.items():
        list[name] = {'!': val['v']}
        recurDeps(list[name], val['d'], master)
    return list


def printDeps(name, dep, indent=''):
    # desc = '{} @{}'.format(name, dep['!'])
    print('%s%s' % (indent, name))
    for sub in sorted(dep):
        if sub != '!':
            printDeps(sub, dep[sub], indent + '|  ')


def matches(key):
    if not ARGS.filter:
        return True
    for s in ARGS.filter:
        if key.startswith(s):
            return True
    return False


def proceedSubdependency(dep):
    if ARGS.filter or ARGS.all:
        return True
    return not dep['u']


def printNormal(master, parsed, indent='  '):
    # C = filter(lambda x: master[x]['u'] is False, master)
    for key in sorted(master):
        if not matches(key):
            continue
        if proceedSubdependency(master[key]):
            printDeps(key, parsed[key], indent)


def printReverse(master, parsed, indent='  '):
    for key in sorted(master):
        if not matches(key):
            continue
        print(indent + key)
        for x, y in sorted(parsed.items()):
            try:
                if y[key]:
                    print(indent + '|  ' + x)
            except KeyError:
                pass


if __name__ == '__main__':
    main()
