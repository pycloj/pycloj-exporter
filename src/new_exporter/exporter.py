import inspect
from writer import save_file, make_src_path
from handlers.module_handler import handle_module_simple, handle_module


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
        return True
    else:
        return False


def should_skip_module(module_name, base_module, element):
    if module_name[0] == "_":
        return True
    elif not is_my_sub_module(base_module, element):
        return True
    return False


def handle_sub_module(src_path, base_module, base_name="", depth=1):
    elements = inspect.getmembers(base_module)
    data = []
    for e in elements:
        if should_skip_module(e[0], base_module, e[1]):
            continue
        elif inspect.ismodule(e[1]):
            handle_sub_module(src_path,
                              e[1],
                              base_name=base_name + "." + e[0],
                              depth=depth + 1)
            print("-" * depth, base_name + "." + e[0])
            handle_module(src_path, base_name, e[0], e[1])


def handle_package(module_name):
    print(module_name)
    the_module = __import__(module_name)
    globals()[module_name] = the_module

    src_path = make_src_path("../../output", module_name,
                             the_module.__version__)
    handle_module(src_path, "", module_name, the_module)
    handle_sub_module(src_path, the_module, base_name=module_name)


if __name__ == "__main__":
    m = "keras"
    handle_package(m)
