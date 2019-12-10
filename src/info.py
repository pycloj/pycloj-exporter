import inspect
import argparse
import pkgutil


def import_all_sub_module(base_module_name):
    import pkgutil
    the_module = __import__(base_module_name)
    globals()[base_module_name] = the_module
    for imp, m, ispkg in pkgutil.walk_packages(path=the_module.__path__):
        if ispkg:
            try:
                mname = f"{base_module_name}.{m}"
                sub_m = __import__(mname)
                globals()[mname] = sub_m
            except:
                print(f"could not import module {m}")


def import_module(module_name, import_sub_module=True):
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
    if import_sub_module:
        import_all_sub_module(module_name)
    return the_module


def get_function(the_module):
  function_list = []
  members = inspect.getmembers(the_module)
  for member in members:
    if inspect.isfunction(member[1]):
        function_list.append(member[0])
  return function_list

def get_class(the_module):
  class_list = []
  members = inspect.getmembers(the_module)
  for member in members:
    if inspect.isclass(member[1]):
        class_list.append(member[0])
  return class_list

def get_submodule(the_module):
  submodule_list = []
  members = inspect.getmembers(the_module)
  for member in members:
    if inspect.ismodule(member[1]):
        submodule_list.append(member[0])
  return submodule_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Info about a python module ")
    parser.add_argument(
        "module", help="Python module for info - make sure it is installed")
    parser.add_argument("--output",
                        help="where to save the output files",
                        default="./../output")

    parser.add_argument("--import_sub_module",
                        type=bool,
                        help="should we import submodules",
                        default=True)
    parser.add_argument(
        '--data',
        default='all',
        const='all',
        choices=['submodules', 'function', 'classes'],
        help='the kind of data we want for the element')

    args = parser.parse_args()
    the_module = import_module(args.module)


    if args.data == "submodules":
      print(get_submodule(the_module))



