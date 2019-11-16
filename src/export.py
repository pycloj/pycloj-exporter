import inspect
import types
import argparse
import os
# from PyInquirer import prompt
from distutils.dir_util import mkpath
import pkgutil
from template import (get_project, get_function, get_source_file_head)

PYCLJ_VERSION = "0.1"

elements_exported = set()

def get_sub_modules(the_module,module_name):
  sub_modules = set()
  for importer, modname, ispkg in pkgutil.walk_packages(path=the_module.__path__):
    # questions = [
    # {
    #     'type': 'confirm',
    #     'name': modname,
    #     'message': f'import sub module {module_name}.{modname}',
    #     'default': False
    # }

    # ]
    # answer = prompt(questions)
    # print (answer)
    # print (type(answer), answer[modname])
    # if answer[modname]:
    #   sub_modules.add(modname)
    sub_modules.add(modname)
  return sub_modules


def get_positional_args(sig):
    params = []
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_ONLY or param.name =="self":
            params.append(param.name)
    return " ".join(params)

def to_clj_types(t):
  if type(t) == bool:
    return 

def get_keyword_args(sig):
    params = []
    defaults = []
    for p in sig.parameters.values():
        if p.kind in [inspect.Parameter.KEYWORD_ONLY,inspect.Parameter.POSITIONAL_OR_KEYWORD] and p.name != "self":
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

    positional_args = get_positional_args(sig)
    kw_args, defaults = get_keyword_args(sig)

    # print("kw_args", kw_args)
    return get_function(module_name,
                        fn_name,
                        positional_args=positional_args,
                        kw_args=kw_args,
                        defaults=defaults,
                        docstring=fn.__doc__)





def handle_class(module_name, src_path, clss_name, clss):
    print("handle_class",module_name, src_path, clss_name, clss)
    data = []
    ignore = ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
    data += handle_function(module_name, clss_name, clss)

  
    data.append(get_function)
    elements = inspect.getmembers(clss)
    for e in elements:
      #skipping members that start with a _
      if e[0][0] == "_":
      #    data+=f";skiping {e[0]} \n" 
        pass
      #TODO: class method
      # elif inspect.ismethod(e[1]):
      #   # res = handle_function(module_name, e[0], e[1])
      #   data+= [f";{e[0]}\n"]
      elif inspect.isfunction(e[1]):
        res = handle_function(module_name, e[0], e[1])
        data+= [res]
        # data+= [f";function {e[0]} {str(e[1])}"]
      elif isinstance(e[1], property):
        # res = handle_function(module_name, e[0], e[1])
        data+= [f";property {e[0]} {e[1]}\n"]
      else:
        # res = handle_function(module_name, e[0], e[1])
        data+= [f";what am I else{e[0]} {e[1]} ?\n"]
      
      


    
    file_head = get_source_file_head(f"{module_name}.{clss_name}", clss_name,
                                     clss.__doc__)
    with open(os.path.join(src_path, f"{clss_name}.clj"), "w") as f:
        f.writelines(file_head)
        for line in data:
          try:
            f.writelines(line)
          except:
            print(line)
            # exit(0)
      


       



def handle_module(module_name,
                            src_path,
                            the_module, base_module=""):
    data = []

    for element in inspect.getmembers(the_module):
        if element[0] in [
                '__builtins__', '__cached__', '__doc__', '__file__',
                '__loader__', '__name__', '__package__', '__path__',
                '__spec__', '__version__'
        ]:
            pass
        elif element in elements_exported:
          continue
        elif element[0] == "__doc__":
            data.append(element[1])
            elements_exported.add(element)
        elif inspect.isclass(element[1]):
            handle_class(module_name, src_path ,element[0], element[1])
        #     elements_exported.add(element)
        # elif inspect.ismethod(element[1]):
        #     data += handle_class_method(the_module, element)
        # elif inspect.isabstract(element[1]):
        #     print(f"{element[0]} is an abstruct class - skip")
        elif inspect.isfunction(element[1]):
            data += handle_function(module_name, element[0],element[1])
            elements_exported.add(element)
    if base_module:
      namespace = f"{base_module}.{module_name}"
    else:
      namespace = module_name
    file_head = get_source_file_head(namespace, module_name,
                                     the_module.__doc__)
    print(src_path,f"{module_name}.clj")
    with open(os.path.join(src_path, f"{module_name}.clj"), "w") as f:
        f.writelines(file_head)
        for line in data:
          f.writelines(line)



def handle_python_lib(module_name, path="", is_root=False, rename_path=True, sub_modules_list=None):
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
    if not sub_modules_list or len(sub_modules_list) == 0:
      sub_modules = get_sub_modules(the_module, module_name)
    else:
      sub_modules = set(sub_modules_list)
    handle_module(module_name,
                            src_path,
                            the_module)
    for m in sub_modules:
      p = mkpath(os.path.join(src_path, m))[0]
      mod = __import__(module_name)
      globals()[m] = mod
      handle_module(m,p, mod, base_module=module_name)


    
    

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
    parser.add_argument("--sub-modules",
                        type=list,
                        help="list of submodule to import",
                        default=[])

    args = parser.parse_args()
    handle_python_lib(args.module, is_root=True, path=args.output, sub_modules_list=args.sub_modules)
