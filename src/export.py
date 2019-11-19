import inspect
import types
import argparse
import os
# from PyInquirer import prompt
from distutils.dir_util import mkpath
import pkgutil
from template import (get_project, get_function, get_source_file_head,
                      get_property, get_class_file_head, get_reference_element,
                      get_reference_member)
from utils import get_sub_modules_recursive

from version import VERSION

classes_exported = set()
classes_members = {}


def create_reference_class(src_path, refering_module, the_class):
    path_list = the_class.__module__.split(".")
    class_name = path_list[-1]
    module_name = ".".join(path_list[:-1])
    full_class_path = ".".join(path_list[:-1])
    mkpath(os.path.join(src_path, refering_module.replace(".", "/")))
    ref_content = get_reference_element(
        f"{refering_module}.{the_class.__name__}", the_class.__module__,
        the_class.__name__)

    members_def = []
    print(classes_members, refering_module, the_class)
    members = classes_members.get(
        f"{the_class.__module__}.{the_class.__name__}",[])
    for m in members:
        members_def.append(
            get_reference_member(
                m, f"{the_class.__module__}.{the_class.__name__}"))

    with open(
            os.path.join(src_path, refering_module.replace(".", "/"),
                         f"{class_name}.clj"), "w") as f:
        f.writelines(ref_content)
        for mdef in members_def:
          f.writelines(mdef)


def get_positional_args(sig):
    params = []
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_ONLY or param.name == "self":
            params.append(param.name)
    return " ".join(params)


def get_keyword_args(sig):
    params = []
    defaults = []
    for p in sig.parameters.values():
        if p.kind in [
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD
        ] and p.name != "self":
            params.append(p.name)
            if p.default != inspect._empty and p.default != None:
                defaults.append(p.name)
                defaults.append(str(p.default).lower())
    print(params)
    print(defaults)
    return " ".join(params), " ".join(defaults)


def handle_function(module_name, fn_name, fn):
    try:
        sig = inspect.signature(fn)
    except Exception as e:
        print(e)
        return ""
    # sig = inspect.signature(fn)
    positional_args = get_positional_args(sig)
    kw_args, defaults = get_keyword_args(sig)

    # print("kw_args", kw_args)
    return get_function(module_name,
                        fn_name,
                        positional_args=positional_args,
                        kw_args=kw_args,
                        defaults=defaults,
                        docstring=fn.__doc__)


def handle_property(module_name, property_name, proprty_el):
    return get_property(module_name,
                        property_name,
                        docstring=proprty_el.__doc__)


def add_class_member(class_path, member):
    print("in class members", class_path,member)
    cls_members = classes_members.get(class_path)
    if not cls_members:
        classes_members[class_path] = []
    classes_members[class_path].append(member)


def handle_class(src_path, the_class):
    data = []
    ignore = [
        '__call__', '__class__', '__delattr__', '__dict__', '__dir__',
        '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
        '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__',
        '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__setstate__',
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__'
    ]

    data.append(get_function)
    elements = inspect.getmembers(the_class)
    path_list = the_class.__module__.split(".")
    class_file = path_list[-1]
    module_name = path_list[-1]
    data += handle_function(module_name, the_class.__name__, the_class)

    for e in elements:
        #skipping members that start with a _
        if e[0][0] == "_":
            pass
        #TODO: class method
        # elif inspect.ismethod(e[1]):
        #   # res = handle_function(module_name, e[0], e[1])
        #   data+= [f";{e[0]}\n"]
        elif inspect.isfunction(e[1]):
            res = handle_function(module_name, e[0], e[1])
            add_class_member(f"{the_class.__module__}.{the_class.__name__}",
                             e[0])
            data += [res]
        elif isinstance(e[1], property):
            res = handle_property(module_name, e[0], e[1])
            add_class_member(f"{the_class.__module__}.{the_class.__name__}",
                             e[0])
            data += res
        else:
            # res = handle_function(module_name, e[0], e[1])
            # data+= [f";what am I else{e[0]} {e[1]} ?\n"]
            pass

    file_head = get_class_file_head(
        f"{the_class.__module__}.{the_class.__name__}", module_name,
        the_class.__module__, the_class.__doc__)
    mkpath(os.path.join(src_path, the_class.__module__.replace(".", "/")))
    with open(
            os.path.join(src_path, the_class.__module__.replace(".", "/"),
                         f"{the_class.__name__}.clj"), "w") as f:
        f.writelines(file_head)
        for line in data:
            try:
                f.writelines(line)
            except:
                print("!!!! failed to write", line)


def handle_module(module_name, src_path, the_module):
    data = []

    for element in inspect.getmembers(the_module):
        if element[0] in [
                '__builtins__', '__cached__', '__doc__', '__file__',
                '__loader__', '__name__', '__package__', '__path__',
                '__spec__', '__version__'
        ]:
            pass
        elif element[0] == "__doc__":
            data.append(element[1])
            #elements_exported.add(element)
        elif inspect.isclass(element[1]):
            if element[1] in classes_exported:
                create_reference_class(src_path, module_name, element[1])
            else:
                handle_class(src_path, element[1])
                create_reference_class(src_path, module_name, element[1])
                classes_exported.add(element[1])

        elif inspect.isfunction(element[1]):
            data += handle_function(module_name, element[0], element[1])
    file_head = get_source_file_head(module_name, module_name,
                                     the_module.__doc__)

    # mkpath(os.path.join(src_path, ))
    if len(data) > 0:
        with open(
                os.path.join(src_path, module_name.replace(".", "/")) + ".clj",
                "w") as f:
            f.writelines(file_head)
            for line in data:
                f.writelines(line)


def handle_python_lib(module_name,
                      path="",
                      is_root=False,
                      rename_path=True,
                      sub_modules_list=None):
    print(f"importing module {module_name}")
    try:
        the_module = __import__(module_name)
    except ModuleNotFoundError:
        print(
            f"could not import module {module_name}. please verify that the module exist"
        )
        print(f"pip install {module_name}")
        print(f"or verify that the right virtualenv is active")
        exit(-1)

    globals()[module_name] = the_module
    version = the_module.__version__
    data = []
    path = os.path.join(path, module_name,
                        f"pyclj-{VERSION}-{module_name}{version}")
    if rename_path and is_root:
        if os.path.exists(path):
            for i in range(50):
                try:
                    os.rename(path, f"{path}__{i}")
                    break
                except:
                    pass
    try:
        mkpath(path)
    except:
        print(f"failed to create path: {path}")
        exit(-1)
    project = get_project(f"pycloj/pycloj-{module_name}",
                          f"{version}--AUTO-{VERSION}-SNAPSHOT")
    # print(project)
    with open(os.path.join(path, "project.clj"), "w") as f:
        f.writelines(project)
    # create src dir
    src_path = os.path.join(path, "src")
    mkpath(src_path)
    # create test dir
    test_path = os.path.join(path, "test")
    mkpath(test_path)
    if not sub_modules_list or len(sub_modules_list) == 0:
        sub_modules, _ = get_sub_modules_recursive(module_name)
    else:
        print(f"modules = {sub_modules_list}")
        sub_modules = set(sub_modules_list)
        sub_modules.add(module_name)
    for m in sub_modules:
        p = mkpath(os.path.join(src_path, m.replace(".", "/")))
        mod = __import__(m)
        globals()[m] = mod
        handle_module(m, src_path, mod)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "Exporting a python module to be used by clojure with libpython-clj")
    parser.add_argument(
        "module",
        help=
        "Python module to export, this module must be install using pip or conda before hand"
    )
    parser.add_argument("--output",
                        help="where to save the output files",
                        default="./../output")
    parser.add_argument("--delete",
                        type=bool,
                        help="delete file and folders if already exist",
                        default=False)
    parser.add_argument(
        "--sub-modules",
        type=str,
        help="list of submodule to import",
        # default=["models"])
        default='')

    args = parser.parse_args()
    
    if args.sub_modules:
      sub_modules = args.sub_modules.split(",")
    else:
      sub_modules = []
    handle_python_lib(args.module,
                      is_root=True,
                      path=args.output,
                      sub_modules_list=sub_modules)
