import inspect
from templates import get_function

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
    # print(defaults)
    return " ".join(params), " ".join(defaults)


def handle_function(module_name, fn_name, fn):
    if fn_name[0] == "_":
        return ""
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