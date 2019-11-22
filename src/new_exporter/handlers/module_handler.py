import inspect
import os

from distutils.dir_util import mkpath
from handlers.func_handler import handle_function
from handlers.class_handler import handle_class
from template import get_source_file_head
from writer import save_file

ignore = [
        '__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
        '__name__', '__package__', '__path__', '__spec__', '__version__',
        "builtins"
    ]

def handle_module_simple(src_path, module_path, module_name, the_module):
  path = module_path.replace(".","/")
  save_file(src_path,path, module_name+".clj",[module_path+"."+module_name])


def handle_module(src_path, module_path, module_name, the_module):
    data = []
    for element in inspect.getmembers(the_module):
        if element[0] in ignore:
            continue
        elif element[0][0] == "_":
            continue
        elif inspect.isclass(element[1]):
            handle_class(src_path, module_name, element[1])
        elif inspect.isfunction(element[1]):
            data.append(handle_function(module_name, element[0], element[1]))

    if len(data) == 0:
      return 
    ns = ".".join([module_path ,module_name])
    file_head = get_source_file_head(ns, module_name, the_module.__doc__)
    path = os.path.join(src_path, module_path.replace(".","/"))
    mkpath(path)
    full_filename = os.path.join(path, f"{module_name}.clj")
    with open(full_filename, "w") as f:
            f.writelines(file_head)
            for line in data:
                f.writelines(line)