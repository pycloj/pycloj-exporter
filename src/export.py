import inspect
import argparse
from writer import save_file, make_src_path
from handlers.module_handler import handle_module_simple, handle_module
from template import get_project
from version import VERSION
import os




def is_my_sub_module(m, sub):
    try:
        # print("is sub module", m.__file__, sub.__file__)
        base_path = m.__file__
        sub_path = sub.__file__
    except:
        return False
    base_path_list = base_path.split("/")
    if base_path_list[-1] == "__init__.py":
        base_path = "/".join(base_path_list[:-1])
    if base_path in sub_path:
        return True
    else:
        return False


def should_skip_module(module_name,
                       base_module,
                       element,
                       ignore_sub_modules=[],
                       only_sub_modules=[]):
    if module_name[0] == "_":
        return True
    elif len(only_sub_modules) > 0:
        if module_name in only_sub_modules:
            return False
        else:
            return True
    elif len(ignore_sub_modules) > 0:
        if module_name in ignore_sub_modules:
            return True
    elif not is_my_sub_module(base_module, element):
        return True
    return False


def handle_sub_module(src_path,
                      base_module,
                      base_name="",
                      only_sub_modules=[],
                      ignore_sub_modules=[],
                      depth=1):
    elements = inspect.getmembers(base_module)
    # data = []
    try:
        for e in elements:
          if should_skip_module(e[0], base_module, e[1]):
              continue
          elif inspect.ismodule(e[1]):
              handle_sub_module(src_path,
                                e[1],
                                base_name=base_name + "." + e[0],
                                depth=depth + 1)
              print("-" * depth, base_name + "." + e[0])
              handle_module(src_path, base_name, e[0], e[1])
    except Exception as e:
      print(e)


def create_project_file(lib_version, module_name, path):
    global VERSION
    project = get_project(f"pycloj/pycloj-{module_name}",
                          f"{lib_version}-AUTO-{VERSION}-SNAPSHOT")
    print(os.path.join(path, "project.clj"))
    with open(os.path.join(path, "project.clj"), "w") as f:
        f.writelines(project)

def handle_package(module_name,
                   path="",
                   only_sub_modules=[],
                   ignore_sub_modules=[]):
    try:
        the_module = __import__(module_name)
    except ModuleNotFoundError:
        print(
            f"could not import module {module_name}. please verify that the module exist"
        )
        print(f"pip install {module_name}")
        print(f"or verify that the right virtualenv is active")
        exit(-1)
    the_module = __import__(module_name)
    globals()[module_name] = the_module

    project_path, src_path = make_src_path(path, module_name, the_module.__version__)
    print (project_path, src_path)
    create_project_file(the_module.__version__, module_name, project_path)
    handle_module(src_path, "", module_name, the_module)
    handle_sub_module(src_path,
                      the_module,
                      base_name=module_name,
                      only_sub_modules=only_sub_modules,
                      ignore_sub_modules=only_sub_modules)
    # print(only_sub_modules)

    # if len(only_sub_modules) > 0:
    #     for m in only_sub_modules:
    #         sub_module = import_sub_module(m)
    #         if sub_module:
    #             handle_sub_module(src_path,
    #                   sub_module,
    #                   base_name=m,
    #                   only_sub_modules=only_sub_modules,
    #                   ignore_sub_modules=only_sub_modules)




def import_sub_module(sub_module_name):
    try:
        sub_module = __import__(sub_module_name)
        globals()[sub_module_name] = sub_module
        return sub_module
    except:
        print(f"could not import {sub_module_name}")
        # exit(0)
        return None

def import_all_sub_module(base_module_name):
    import pkgutil
    the_module = __import__(base_module_name)
    globals()[base_module_name] = the_module
    for imp, m, ispkg in pkgutil.walk_packages(path=the_module.__path__):
        if ispkg:
            try:
                mname = f"{base_module_name}.{m}"
                sub_m = __import__(mname)
                globals()[mname]= sub_m 
            except:
                print(f"could not import module {m}")


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

    parser.add_argument(
        "--only-sub-modules",
        type=str,
        help=
        "list of submodule to import seprated by a comma, all other submodules will be ignored",
        # default=["models"])
        default='')
    parser.add_argument(
        "--ignore-sub-modules",
        type=str,
        help=
        "list of submodule to ignore seprated by a comma, all other submodules will be included",
        # default=["models"])
        default='')

    args = parser.parse_args()

    if args.only_sub_modules:
        only_sub_modules = args.only_sub_modules.split(",")
        print(only_sub_modules)
        for m in only_sub_modules:
            import_sub_module(m)
    else:
        import_all_sub_module(args.module)
        only_sub_modules = []
        
    if args.ignore_sub_modules:
        ignore_sub_modules = args.ignore_sub_modules.split(",")
    else:
        ignore_sub_modules = []

    handle_package(args.module,
                   path=args.output,
                   only_sub_modules=only_sub_modules,
                   ignore_sub_modules=ignore_sub_modules)
