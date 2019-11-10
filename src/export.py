import inspect
import types
import argparse
import os



def wrap_docstring(txt):
  return f"\"{txt}\""

def has_positional_args(sig):
  for param in sig.parameters.values():
    if param._kind == "POSITIONAL_ONLY":
      return True
  return False

def get_positional_args(sig):
  params = []
  for param in sig.parameters.values():
    if param._kind == "POSITIONAL_ONLY":
      params.append(param.name)
  return params

def has_keyward_args(sig):
  has =False
  for param in sig.parameters.values():
    if param._kind in ["POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"]:
      has =  True
  return has

def get_keyword_args(sig):
  params = []
  defaults = []
  for param in sig.parameters.values():
    if param._kind in ["POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"]:
      params.append(param.name)
      if params.default is not None:
        defaults.append(params.name)
        defaults.append(params.default)
        
  return params, defaults



def get_function_signature(fn):
  return inspect.signature(fn)



def handle_function(module, element):
  data = []
  sig = get_function_signature(element[1])
  print(sig)
  data.append(f"({element[0]} ")
  if has_positional_args(sig):
    position_args = get_positional_args(sig)
    data.append(f"[{position_args} ")
  if get_keyword_args(sig):
    keyword_args, defaults = get_keyword_args(sig)
    data.append(f" & {{ :keys [{keyword_args}] ")
    if len(defaults) > 0:
      data.append(f" :or {{ {defaults} }} ")
    #close keyword params
    data.append("}}")

  #close params
  data.append("]\n")
  data.append(
    wrap_docstring(element[1].__doc__)
    )
  #implementation
  if has_keyward_args(sig):
    data.append("(py/call-attr-kw {module.__name__} \"{element[0]}\"  [{position_args} ] {{ {keyword_args} }} )")
  else:
    data.append("(py/call-attr-kw {module.__name__} \"{element[0]}\"  {position_args}  )")
  #close function
  data.append(")")

  
  return data
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
  

def handle_module(module_name, path="", is_root=False):
  print(f"importing module {module_name}")
  try:
    the_module = __import__(module_name)
  except:
    return None
  globals()[module_name] = the_module
  path = os.path.join(path, module_name)
  os.mkdir(path)
  data = []
  
  for element in inspect.getmembers(the_module):
    if element[0] == "__version__":
      version = element[1]
    if element[0] == "__builtins__":
      pass
    elif element[0] == "__doc__":
      data.append(element[1])
    # elif inspect.ismodule(element[1]):
    #   handle_module(f"{module_name}.{element[0]}",path,is_root=False)
    elif inspect.isclass(element[1]):
      data += handle_class(the_module, element)
    elif inspect.ismethod(element[1]):
      data += handle_class_method(the_module, element)
    elif inspect.isabstract(element[1]):
      print(f"{element[0]} is an abstruct class - skip")
    elif inspect.isfunction(element[1]):
      data += handle_function(the_module, element)    
  os.mkdir(os.path.join(path, module_name))
  with open(os.path.join(path, f"{module_name}.clj"), 'w') as f:
    for l in data:
      if l:
        f.writelines(l)
  



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exporting a python module to be used by clojure with libpython-clj")
    parser.add_argument("module", help="Python module to export, this module must be install using pip or conda before hand")
    parser.add_argument("--output", help="where to save the output files",default="./../output")
    
    args = parser.parse_args()
    handle_module(args.module, is_root=True, path= args.output)


