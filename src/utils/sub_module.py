import pkgutil



def get_sub_module(the_module,module_name, sub_module_set, skip_underscore=True):
  
  for importer, modname, ispkg in pkgutil.walk_packages(path=the_module.__path__):
    if modname[0] == "_" and skip_underscore:
      pass
    else:
      sub_module_set.add(f"{module_name}.{modname}")

def get_next_level(the_module,module_name,current_sub_module_set, next_sub_module_set, skip_underscore=True):
    for m in current_sub_module_set:
      try:
        mod = __import__(m)
        globals()[m] = mod
        get_sub_module(mod,m, next_sub_module_set, skip_underscore)
      except:
        pass

def is_importable(mlist):
  imp_mod = set()
  for m in mlist:
    try:
      mod = __import__(m)
      imp_mod.add(m)
    except:
      pass
  return imp_mod

def get_sub_modules_recursive(module_name,skip_underscore=True, level=4):
    sub_modules_0 = set()
    sub_modules_1 = set()
    sub_modules_2 = set()
    sub_modules_3 = set()
    sub_modules_4 = set()
    
    a = set()
    try:
      mod = __import__(module_name)
      globals()[module_name] = mod
      sub_modules_0.add(module_name)
    except:
      pass
    if level > 0:
      get_next_level(mod,module_name,sub_modules_0, sub_modules_1, skip_underscore)
    if level > 1:
      get_next_level(mod,module_name,sub_modules_1, sub_modules_2, skip_underscore)
    if level > 2:
      get_next_level(mod,module_name,sub_modules_2, sub_modules_3, skip_underscore)
    if level > 3:
      get_next_level(mod,module_name,sub_modules_3, sub_modules_4, skip_underscore)
    a = sub_modules_0 | sub_modules_1 |sub_modules_2 |sub_modules_3
    return is_importable(a), a



  


if __name__ == "__main__":
  importable, _all_modules = get_sub_modules_recursive("keras", level=4)
  print(len(_all_modules))#, _all_modules)
  print(len(importable), importable)