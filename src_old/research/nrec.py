import inspect
import keras


def common_path(path,name):
  p_list = path.split('/')
    
    



def get_sub_module(element, depth=0):
    if depth > 2:
        return
    for e in inspect.getmembers(element):
        # print(e[0],type(e[1]))
        if e[0] in [
                '__builtins__', '__cached__', '__doc__', '__file__',
                '__loader__', '__name__', '__package__', '__path__',
                '__spec__', '__version__', 'absolute_import'
        ]:
            pass
        elif e[0][0] == "_":
            pass
        try:
          f = e[1].__file__
          print(e[0],f)
          if inspect.ismodule(e[1]):
              # print(f"{e[0]} is a module")
              get_sub_module(e[1], depth + 1)
        except:
          pass


get_sub_module(keras)