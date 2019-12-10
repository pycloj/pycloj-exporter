import inspect
import argparse
import pkgutil


def protect_docstring(dstr):
    if dstr and type(dstr) == str:
        return dstr.replace('"', '\\"')
    else:
        return ""

def import_all_sub_module(base_module_name):
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


def get_functions(the_module):
    function_list = []
    members = inspect.getmembers(the_module)
    for member in members:
        if inspect.isfunction(member[1]):
            function_list.append(member[0])
    return function_list


def get_classes(the_module):
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

def empty_or_val(val):
  if val == inspect._empty:
    return None
  return val

def king_to_str(kind):
  return str(kind).split(".")[-1]
def get_function_info(fn):
    args = []

    generator = inspect.isgeneratorfunction(fn)
    is_async = inspect.iscoroutine(fn)
    awaitable = inspect.isawaitable(fn)
    isbuiltin = inspect.isbuiltin(fn)

    sig = inspect.signature(fn)
    for p in sig.parameters.values():
        args.append({
            "name": empty_or_val(p.name),
            "empty": empty_or_val(p.empty),
            "kind": king_to_str(p.kind),
            "default": empty_or_val(p.default),
            "annotation": empty_or_val(p.annotation),
        })
    return {
        "args": args,
        "name": fn.__name__,
        "return_annotation": empty_or_val(sig.return_annotation),
        "doc": protect_docstring(fn.__doc__),
        "generator":generator,
        "async":is_async,
        "awaitable":awaitable,
        "builtin":isbuiltin,
    }

# import keras
# print(get_function_info(keras.Input))

def get_class_members(the_class):
    class_members = []
    class_functions = []
    class_methods = []
    class_properties = []
    members = inspect.getmembers(the_class)
    for member in members:
      if inspect.isfunction(member[1]):
        class_functions.append(get_function_info(member[1]))
      elif inspect.ismethod(member[1]):
        class_methods.append(get_function_info(member[1]))
      elif isinstance(member[1], property):
        class_properties.append(member[0])
      else:
        class_members.append(member[0])
    
    return {
      "module":the_class.__module__,
      "name":the_class.__name__,
      "members": class_members,
      "methods": class_methods,
      "functions": class_functions,
      "properties": class_properties,
      "doc": protect_docstring(the_class.__doc__)
    }



# import keras
# print(get_class_members(keras.Sequential))

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
    parser.add_argument('--data',
                        default='all',
                        choices=['submodules', 'functions', 'classes', 'all'],
                        help='the kind of data we want for the element')

    args = parser.parse_args()
    the_module = import_module(args.module)

    if args.data == "submodules":
        print("--submodules--")
        print(get_submodule(the_module))
    if args.data == "functions":
        print("--functions--")
        print(get_functions(the_module))
    if args.data == "classes":
        print("--classes--")
        print(get_classes(the_module))
    if args.data == "all":
        print("--submodules--")
        print(get_submodule(the_module))
        print("--functions--")
        print(get_functions(the_module))
        print("--classes--")
        print(get_classes(the_module))
