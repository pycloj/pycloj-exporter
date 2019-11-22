import inspect
import os
from handlers.function_handler import handle_function
from template import get_class_file_head, get_property
from distutils.dir_util import mkpath


def handle_property(module_name, property_name, proprty_el):
    return get_property(module_name,
                        property_name,
                        docstring=proprty_el.__doc__)


def handle_class(src_path, class_name, the_class, base_path):
    data = []
    ignore = [
        '__call__', '__class__', '__delattr__', '__dict__', '__dir__',
        '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
        '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__',
        '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__setstate__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__', "builtins"
    ]
    elements = inspect.getmembers(the_class)
    module_name = ".".join([src_path, class_name])
    data.append(handle_function(module_name, class_name, the_class))
    for e in elements:
        if e[0][0] == "_":
            continue
        if e[0] in ignore:
            continue
        elif inspect.isfunction(e[1]):
            res = handle_function(module_name, e[0], e[1])
            data.append(res)
        elif isinstance(e[1], property):
            res = handle_property(module_name, e[0], e[1])
            data.append(res)
    file_head = get_class_file_head(f"{base_path}.{class_name}", base_path,
                                    base_path, the_class.__doc__)

    mkpath(os.path.join(src_path, base_path.replace(".", "/"), class_name))
    with open(os.path.join(src_path, base_path.replace(".", "/"),
                         f"{class_name}.clj"), "w") as f:
        f.writelines(file_head)
        for line in data:
            f.writelines(line)
