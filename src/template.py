

from templates import (method_positional, 
                                  method_kw,
                                  method_kw_defaults, 
                                  method_positional_kw, 
                                  method_positional_kw_defaults, 
                                  project_tpl,
                                  source_file_head
                                  )

def get_project(project, version):
  return project_tpl.substitute({"project":project, "version":version})


def get_source_file_head(namespace, module_name, docstring):
  return source_file_head.substitute({"namespace":namespace, "module_name":module_name,"docstring":docstring})

def get_function(module_name, function_name, positional_args="", kw_args="", defaults="", docstring=""):
  if positional_args and kw_args and defaults:
    return method_positional_kw_defaults.substitute({
      "docstring":docstring,
      "function_name":function_name,
      "module_name":module_name,
      "positional_args":positional_args,
      "kw_args":kw_args,
      "defaults":defaults
    })
  elif positional_args and kw_args:
    return method_positional_kw.substitute({
      "module_name":module_name,
      "function_name":function_name,
      "docstring":docstring,
      "positional_args":positional_args,
      "kw_args":kw_args
    })
  elif  defaults and kw_args:
    return method_kw_defaults.substitute({
      "module_name":module_name,
      "function_name":function_name,
      "docstring":docstring,
      "positional_args":positional_args,
      "kw_args":kw_args,
      "defaults":defaults
    })
  elif kw_args:
    return method_kw.substitute({
      "module_name":module_name,
      "function_name":function_name,
      "docstring":docstring,
      "kw_args":kw_args
    })
  elif positional_args:
    return method_positional.substitute({
      "module_name":module_name,
      "function_name":function_name,
      "docstring":docstring,
      "positional_args":positional_args
    })
  else:
      return method_positional.substitute({
      "module_name":module_name,
      "function_name":function_name,
      "docstring":docstring,
      "positional_args":positional_args
    })



if __name__ == "__main__":
  print(get_source_file_head("keras", "keras"))
  print(get_function("keras", "input", positional_args="a b c"))
  print(get_function("keras", "input", positional_args="a b c", kw_args = "d e f"))
  print(get_function("keras", "input", positional_args="a b c", kw_args = "d e f", defaults="e 1 f 2"))
  print(get_function("keras", "input", positional_args="a b c",docstring="some docstring"))