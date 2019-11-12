import inspect
import types
import argparse
import os
from distutils.dir_util import mkpath
import pkgutil
from template import (get_project, get_function, get_source_file_head)

PYCLJ_VERSION = "0.1"

sub_modules = set()

def get_positional_args(sig):
    params = []
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            params.append(param.name)
    return " ".join(params)

def to_clj_types(t):
  if type(t) == bool:
    return 

def get_keyword_args(sig):
    params = []
    defaults = []
    for p in sig.parameters.values():
        print(p.kind)
        if p.kind in [inspect.Parameter.KEYWORD_ONLY,inspect.Parameter.POSITIONAL_OR_KEYWORD]:
            params.append(p.name)
            if p.default is not None:
                defaults.append(p.name)
                defaults.append(str(p.default).lower())
    print(params)
    print(defaults)
    return " ".join(params), " ".join(defaults)


def handle_function(the_module, module_name, element):
    sig = inspect.signature(element[1])
    print(sig)
    positional_args = get_positional_args(sig)
    kw_args, defaults = get_keyword_args(sig)

    print("kw_args", kw_args)
    return get_function(module_name,
                        element[0],
                        positional_args=positional_args,
                        kw_args=kw_args,
                        defaults=defaults,
                        docstring=element[1].__doc__)


def handle_class(module, element):
    data = []
    data.append(element[1].__doc__)
    return data


def handle_class_method(module, element):
    data = []
    data.append(element[1].__doc__)
    return data


def is_globals(module, name):
    pass




def handle_module(the_module, module_name, src_path, test_path, is_root=False):
    file_head = get_source_file_head(module_name, module_name,
                                     the_module.__doc__)
    data = []
    for element in inspect.getmembers(the_module):
        if element[0] in [
                '__builtins__', '__cached__', '__doc__', '__file__',
                '__loader__', '__name__', '__package__', '__path__',
                '__spec__', '__version__'
        ]:
            pass
        elif inspect.ismodule(element[1]):
          print("module  name = ", element[1].__name__)
          sub_module_name = element[1].__name__
          try:
              ""
              sub_module = __import__(sub_module_name)
          except ModuleNotFoundError:
              print(
                  f"could not import module {sub_module_name} "
              )
              # print(f"pip install {module_name}")
              # print(f"or verify that the right virtualenv is active")
              exit(-1)
          handle_module(sub_module, f"{module_name}.{sub_module_name}",src_path,test_path,is_root=False)

        # elif inspect.isclass(element[1]):
        #   data += handle_class(the_module, element)
        # elif inspect.ismethod(element[1]):
        #   data += handle_class_method(the_module, element)
        # elif inspect.isabstract(element[1]):
        #   print(f"{element[0]} is an abstruct class - skip")
        elif inspect.isfunction(element[1]):
            data += handle_function(the_module,module_name, element)
    with open(os.path.join(src_path, f"{module_name}.clj"), "w") as f:
        f.writelines(file_head)
        f.writelines(data)


def create_sub_elements_new(the_module,
                            module_name,
                            src_path,
                            test_path,
                            is_root=False):
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
        elif inspect.ismodule(element[1]):
            handle_module(f"{module_name}.{element[0]}", path, is_root=False)
        elif inspect.isclass(element[1]):
            data += handle_class(the_module, element)
        elif inspect.ismethod(element[1]):
            data += handle_class_method(the_module, element)
        elif inspect.isabstract(element[1]):
            print(f"{element[0]} is an abstruct class - skip")
        elif inspect.isfunction(element[1]):
            data += handle_function(the_module, element)




def handle_python_lib(module_name, path="", is_root=False, rename_path=True):
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
                        f"pyclj-{PYCLJ_VERSION}-{module_name}{version}")
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
    project = get_project(f"pyclj-{module_name}", version)
    # print(project)
    with open(os.path.join(path, "project.clj"), "w") as f:
        f.writelines(project)
    # create src dir
    src_path = os.path.join(path, "src")
    mkpath(src_path)
    # create test dir
    test_path = os.path.join(path, "test")
    mkpath(test_path)
    
    

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

    args = parser.parse_args()
    handle_python_lib(args.module, is_root=True, path=args.output)
