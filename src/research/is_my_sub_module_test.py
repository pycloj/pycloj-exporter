import inspect


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
        # print("FOUND", m.__file__, sub.__file__)
        return True
    else:
        return False


def handle_sub_module(base_module,base_name="", depth=1):
  elements = inspect.getmembers(base_module)
  for e in elements:
    if inspect.ismodule(e[1]) and e[0][0] !="_":
      if is_my_sub_module(base_module, e[1]):
        print("-"* depth, base_name+"."+e[0])
        handle_sub_module(e[1], base_name=base_name+"."+e[0], depth=depth+1)
    # else:
    #   if e[0][0] != "_":
    #     print("++"*depth, e[0])
      






def handle_package(module_name):
  print(module_name)
  the_module = __import__(module_name)
  globals()[module_name] = the_module
  handle_sub_module(the_module, base_name=module_name)

m = "sklearn"
handle_package(m)

