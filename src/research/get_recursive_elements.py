import argparse
import inspect


modules = set()
classes = set()
functions = set()
others = set()

ignore = set(['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__version__', 'absolute_import'])

recurssion = 0

def collect_elements(the_module):
    elements = inspect.getmembers(the_module)
    for e in elements:
      if e[0] in ignore:
        pass
      elif inspect.ismodule(e[1]):
        if e[1] in modules:
          pass
        else:
          modules.add(e[1])
      elif inspect.isclass(e[1]):
        if e[1] in classes:
          pass
        else:
          classes.add(e[1]) 
      elif inspect.isfunction(e[1]):
        if e[1] in functions:
          pass
        else:
          functions.add(e[1]) 
      else:
        pass
        # print(e[0])
          # if e[1] in others:
          #   pass
          # else:
          #   others.add(e[1])

    print(modules)
    print(classes)
    print(functions)
    print(others)
    


def rescan_modules(the_module = None):
    if the_module:
      sub_elements = inspect.getmembers(the_module)
    else:
    
      sub_elements = inspect.getmembers(m)
    for se  in sub_elements:
      if type(se[1]) in [dict, str, int]:
        pass
      elif se[1] not in classes and se[1] not in functions and se[1] not in modules:
        collect_elements(se[1])

      

def handle_python_lib(module_name):
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
    collect_elements(the_module)

    
    
      


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=
        "Exporting a python module to be used by clojure with libpython-clj")
    parser.add_argument(
        "module",
        help=
        "Python module to export, this module must be install using pip or conda before hand"
    )
    

    args = parser.parse_args()
    handle_python_lib(args.module)