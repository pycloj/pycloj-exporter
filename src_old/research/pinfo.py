#!/usr/bin/env python

import os, sys
import pkgutil

def list_submodules(list_name, package_name):
    for loader, module_name, is_pkg in pkgutil.walk_packages(package_name.__path__, package_name.__name__+'.'):
        list_name.append(module_name)
        module_name = __import__(module_name, fromlist='dummylist')
        if is_pkg:
            list_submodules(list_name, module_name)

if len(sys.argv) != 2:
    print('Usage: {} [PACKAGE-NAME]'.format(os.path.basename(__file__)))
    sys.exit(1)
else:
    package_name = sys.argv[1]

try:
    package = __import__(package_name)
except ImportError:
    print('Package {} not found...'.format(package_name))
    sys.exit(1)


all_modules = []
list_submodules(all_modules, package)

print(all_modules)