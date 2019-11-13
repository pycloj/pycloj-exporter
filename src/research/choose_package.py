import pkgutil
import keras
from pprint import pprint
from PyInquirer import prompt

sub_modules = set()

for importer, modname, ispkg in pkgutil.walk_packages(path=keras.__path__):
    sub_modules.add(modname)
    questions = [
    {
        'type': 'confirm',
        'name': modname,
        'message': f'import sub module keras.{modname}',
        'default': False
    }

    ]
    answer = prompt(questions)
    print (type(answer), answer['activations'])


