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


LIBROOT = ""
MODULE_NAME = ""

def get_sub_module_path(fname):
  global LIBROOT, MODULE_NAME
  remove_prefix = fname[len(LIBROOT)+1:-3]
  plist = remove_prefix.split("/")
  path = "/".join(plist[:-1])
  file_name = plist[-1]
  if file_name == "__init__":
    try:
      file_name = plist[-2]
    except:
      file_name = MODULE_NAME
  return path, file_name


def get_ns_from_path(fname):
  global LIBROOT, MODULE_NAME
  path, filename = get_sub_module_path(fname)
  module_name = LIBROOT.split("/")[-1]
  path = path.replace("/",".")
  return f"{module_name}.{path}.{filename}"



def create_reference_class(src_path, refering_module, the_class):
    print("create_reference_class", refering_module,the_class )
    path_list = the_class.__module__.split(".")
    class_name = path_list[-1]
    module_name = ".".join(path_list[:-1])
    full_class_path = ".".join(path_list[:-1])
    mkpath(os.path.join(src_path, refering_module.replace(".", "/")))
    ref_content = get_reference_element(
        f"{refering_module}.{the_class.__name__}", the_class.__module__,
        the_class.__name__)

    members_def = []
    # print(classes_members, refering_module, the_class)
    members = classes_members.get(
        f"{the_class.__module__}.{the_class.__name__}", [])
    for m in members:
        members_def.append(
            get_reference_member(
                m, f"{the_class.__module__}.{the_class.__name__}"))

    with open(
            os.path.join(src_path, refering_module.replace(".", "/"),
                         f"{the_class.__name__}.clj"), "w") as f:
        f.writelines(ref_content)
        for mdef in members_def:
            f.writelines(mdef)


def get_positional_args(sig):
    params = []
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_ONLY or param.name == "self":
            params.append(param.name)
    return " ".join(params)

def get_default_arg_value(default_val):
  if type(default_val) == str:
    return f'\"{default_val}\"'
  elif type(default_val) == bool:
    return str(default_val).lower()
  elif type(default_val) == list:
    return str(default_val)
  else:
    return str(default_val)




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
                defaults.append(get_default_arg_value(p.default))
    #print(params)
    print(defaults)
    return " ".join(params), " ".join(defaults)


def handle_function(module_name, fn_name, fn):
    try:
        sig = inspect.signature(fn)
    except Exception as e:
        #print(e)
        return ""
    # sig = inspect.signature(fn)
    positional_args = get_positional_args(sig)
    kw_args, defaults = get_keyword_args(sig)

    # #print("kw_args", kw_args)
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
    #print("in class members", class_path,member)
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
        '__sizeof__', '__str__', '__subclasshook__', '__weakref__',"builtins"
    ]

    elements = inspect.getmembers(the_class)
    path_list = the_class.__module__.split(".")
    class_file = path_list[-1]
    module_name = path_list[-1]
    data.append(handle_function(module_name, the_class.__name__, the_class))

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
            data.append(res)
        elif isinstance(e[1], property):
            res = handle_property(module_name, e[0], e[1])
            add_class_member(f"{the_class.__module__}.{the_class.__name__}",
                             e[0])
            data.append(res)
        else:
            # res = handle_function(module_name, e[0], e[1])
            # data+= [f";what am I else{e[0]} {e[1]} ?\n"]
            pass

    file_head = get_class_file_head(
        f"{the_class.__module__}.{the_class.__name__}", module_name,
        the_class.__module__, the_class.__doc__)
    mkpath(os.path.join(src_path, the_class.__module__.replace(".", "/")))
    #print(data)
    with open(
            os.path.join(src_path, the_class.__module__.replace(".", "/"),
                         f"{the_class.__name__}.clj"), "w") as f:
        f.writelines(file_head)
        for line in data:
            # try:
            #print(line, type(line))
            f.writelines(line)
            # except:
            # print("!!!! failed to write", line)


def handle_module(module_name, src_path, the_module,  depth=0, handle_sub_module=True):
    if depth > 1:
        return
    data = []
    # print(the_module)
    # exit(0)
    ignore = [
            '__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
            '__name__', '__package__', '__path__', '__spec__', '__version__',"builtins"
        ]
    for element in inspect.getmembers(the_module):

        # print(element[0])
        if element[0] in ignore:
            # print("ignoring", element[0])
            pass
        elif element[0] == "__doc__":
            data.append(element[1])
            
        elif inspect.isclass(element[1]):
            if element[1] in classes_exported:
                create_reference_class(src_path, module_name, element[1])
            else:
                handle_class(src_path, element[1])
                create_reference_class(src_path, module_name, element[1])
                classes_exported.add(element[1])

        elif inspect.isfunction(element[1]):
            # print("function", element[0])
            data.append(handle_function(module_name, element[0], element[1]))
        elif inspect.ismodule(element[1]) and handle_sub_module:
            try:
              if LIBROOT in element[1].__file__:
                handle_module(element[0],src_path,element[1],depth+1)
            except:
              pass
        else:
            # print("in else", element[0], type(element[1]))
            pass
    
    

    try:
      filepath = the_module.__file__
    except:
      return 

    ns = get_ns_from_path(filepath)
    file_head = get_source_file_head(ns, module_name,
                                     the_module.__doc__)
    fpath, filename = get_sub_module_path(filepath)
    path = os.path.join(src_path, fpath )
    mkpath(path)
    full_filename = os.path.join(path, f"{filename}.clj")
    if len(data) > 0:
        with open(full_filename,"w") as f:
            f.writelines(file_head)
            for line in data:
                f.writelines(line)


def handle_base_module(module_name, src_path, the_module):
    data = []
    ignore = [
            '__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
            '__name__', '__package__', '__path__', '__spec__', '__version__',"builtins"
        ]
    for element in inspect.getmembers(the_module):
        if element[0] in ignore:
            pass
        elif element[0] == "__doc__":
            data.append(element[1])
        elif inspect.isclass(element[1]):
            if element[1] in classes_exported:
                create_reference_class(src_path, module_name, element[1])
            else:
                handle_class(src_path, element[1])
                create_reference_class(src_path, module_name, element[1])
                classes_exported.add(element[1])

        elif inspect.isfunction(element[1]):
            # print("function", element[0])
            data.append(handle_function(module_name, element[0], element[1]))
    
    



    
    full_filename = os.path.join(src_path, f"{module_name}.clj")
    file_head = get_source_file_head(module_name, module_name,
                                     the_module.__doc__)

    with open(full_filename,"w") as f:
        f.writelines(file_head)
        for line in data:
            f.writelines(line)




def handle_python_lib(module_name,
                      path="",
                      is_root=False,
                      rename_path=True,
                      sub_modules_list=[]):
    global  LIBROOT, MODULE_NAME
    MODULE_NAME = module_name
    print(f"importing module {module_name}")
    try:
        the_module = __import__(module_name)
        LIBROOT = the_module.__path__[0]
        # print("LIBROOT",LIBROOT)
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
        # print(f"failed to create path: {path}")
        exit(-1)
    project = get_project(f"pycloj/pycloj-{module_name}",
                          f"{version}-AUTO-{VERSION}-SNAPSHOT")
    # print(project)
    with open(os.path.join(path, "project.clj"), "w") as f:
        f.writelines(project)
    # create src dir
    src_path = os.path.join(path, "src")
    mkpath(src_path)
    # create test dir
    test_path = os.path.join(path, "test")
    mkpath(test_path)
    handle_base_module(module_name, src_path, the_module)
    #debug
    for elm in inspect.getmembers(the_module):
        # if inspect.ismodule(elm[1]) and elm[0] == "datasets":
        if inspect.ismodule(elm[1])  :
            if len(sub_modules_list)==0:
                handle_module(elm[0], src_path + "/" + module_name, elm[1])
            elif elm[0] in  sub_modules_list:
                handle_module(elm[0], src_path + "/" + module_name, elm[1])



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
