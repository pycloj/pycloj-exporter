import inspect
import os
from handlers.function_handler import handle_function
from template import get_class_file_head, get_property
from distutils.dir_util import mkpath


def handle_property(module_name, property_name, proprty_el):
    return get_property(module_name,
                        property_name,
                        docstring=proprty_el.__doc__)


def handle_class(src_path, class_name, the_class, base_path, module_name,
                 the_module):
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
    if not base_path:
        namespace = ".".join([module_name, class_name])
        full_import_path = module_name
    else:
        namespace = ".".join([base_path, module_name, class_name])
        full_import_path = ".".join([base_path, module_name])

    data.append(handle_function(module_name, class_name, the_class, constractor=True))
    for e in elements:
        if e[0][0] == "_":
            continue
        if e[0] in ignore:
            continue
        elif inspect.isfunction(e[1]):
            res = handle_function(module_name, e[0], e[1], class_member=True)
            data.append(res)
        elif isinstance(e[1], property):
            res = handle_property(module_name, e[0], e[1])
            data.append(res)
    print(f"{base_path}.{class_name}", base_path, base_path)

    module_name = the_module.__name__
    last_module_part = module_name.split(".")[-1]
    file_head = get_class_file_head(module_name, class_name, last_module_part,
                                    the_class.__doc__)

    mkpath(os.path.join(src_path, module_name.replace(".", "/")))
    with open(
            os.path.join(src_path, module_name.replace(".", "/"),
                         f"{class_name}.clj"), "w") as f:
        f.writelines(file_head)
        for line in data:
            f.writelines(line)
