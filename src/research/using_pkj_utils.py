import pkgutil
import tensorflow
import keras

# for m in pkgutil.iter_modules(keras.__path__):
#    i+=1
#    print(i,m)

sub_modules = set()

for importer, modname, ispkg in pkgutil.walk_packages(path=keras.__path__):
  if ispkg:
    sub_modules.add(modname)
  else:
    print (f"{modname} is not a package")
print(sub_modules)
# import keras.activations 
# for m in pkgutil.iter_modules(keras.activations.__path__):
#   print(m)

# for sm in sub_modules:
#   the_module = __import__(f"keras.{sm}")

# for m in pkgutil.iter_importers('keras'):
#   print(m)

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
