import pkgutil




def get_sub_module_rec(the_module,module_name, sub_module_set, skip_underscore=True):
  
  for importer, modname, ispkg in pkgutil.walk_packages(path=the_module.__path__):
    if modname[0] == "_" and skip_underscore:
      pass
    else:
      sub_module_set.add(f"{module_name}.{modname}")




if __name__ == "__main__":
  import pandas
  sub_modules_0 = set()
  sub_modules_1 = set()
  sub_modules_2 = set()
  sub_modules_3 = set()


  get_sub_module_rec(pandas ,"pandas", sub_modules_0)
  for m in sub_modules_0:
    try:
      mod = __import__(m)
      globals()[m] = mod
      get_sub_module_rec(mod,m, sub_modules_1)
    except:
      pass
  for m in sub_modules_1:
    try:
      mod = __import__(m)
      globals()[m] = mod
      get_sub_module_rec(mod,m, sub_modules_2)
    except:
      pass
  for m in sub_modules_2:
    try:
      mod = __import__(m)
      globals()[m] = mod
      get_sub_module_rec(mod,m, sub_modules_3)
    except:
      pass
  # print(0, sub_modules_0)
  # print(1, sub_modules_1)
  # print(2, sub_modules_2)
  # print(3, sub_modules_3)
  all = sub_modules_0 | sub_modules_1 |sub_modules_2 |sub_modules_3
  print(all)
  print(len(all))