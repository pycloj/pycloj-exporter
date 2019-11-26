import inspect
from template import get_function, get_function_new


def get_default_arg_value(default_val):
    if type(default_val) == str:
        return f'\"{default_val}\"'
    elif type(default_val) == bool:
        return str(default_val).lower()
    elif type(default_val) == list:
        return str(default_val)
    else:
        return str(default_val)


def get_args(sig):
    kw = []
    defaults = []
    positional  = []
    first_default = False
    for p in sig.parameters.values():
        if p.kind in [
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD
        ] and p.name != "self":
            if p.default == inspect._empty and not first_default:
              positional.append(p.name)
            else:
              first_default = True
              kw.append(p.name)
              if p.default != inspect._empty and p.default != None:
                defaults.append(p.name)
                defaults.append(get_default_arg_value(p.default))
    return  " ".join(positional), " ".join(kw), " ".join(defaults),
  


def should_skip_function(func_name, base_module, func):
    if func_name[0] == "_":
        return True
    return False


def handle_function(module_name, fn_name, fn, class_member=False,constractor=False):
    if fn_name[0] == "_":
        return ""
    try:
        sig = inspect.signature(fn)
    except Exception as e:
        #print(e)
        return ""
    positional_args, kw_args, defaults = get_args(sig)
    # #print("kw_args", kw_args)
    return get_function_new(module_name,
                        fn_name,
                        positional_args=positional_args,
                        kw_args=kw_args,
                        defaults=defaults,
                        docstring=fn.__doc__,
                        class_member=class_member)
