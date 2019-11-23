from templates import (method_positional, method_kw, method_kw_defaults,
                       method_positional_kw, method_positional_kw_defaults,
                       project_tpl, source_file_head, class_file_head,
                       property_tpl, reference_element_tpl, reference_member_tpl)





def protect_docstring(dstr):
  if dstr and type(dstr) == str:
    return dstr.replace('"','\\"')
  else:
    return ""

def kwargs_to_call_format(kwargs_str):
    kw_args = kwargs_str.split(" ")
    call_format = ""
    for a in kw_args:
        call_format += f":{a} {a} "
    return call_format


def py2clojure_function_name(fname):
    # return fname.loawer().replace("_","-")
    return fname.replace("_", "-")


def get_project(project, version):
    return project_tpl.substitute({"project": project, "version": version})


def get_source_file_head(namespace, module_name, docstring):
    return source_file_head.substitute({
        "namespace":namespace,
        "module_name": module_name,
        "clj_module_name": py2clojure_function_name(module_name),
        "docstring": protect_docstring(docstring),
        "clj_namespace": py2clojure_function_name(namespace)

    })


def get_class_file_head(module_name,class_name, last_module_part, docstring):
    return class_file_head.substitute({
        "module_name": module_name,
        "module_name_clj": py2clojure_function_name(module_name),
        "class_name": class_name,
        "class_name_clj": py2clojure_function_name(class_name),
        "last_module_part": last_module_part,
        "last_module_part_clj": py2clojure_function_name(last_module_part),
        "docstring": protect_docstring(docstring),
    })


def get_property(module_name, property_name, docstring=""):
    return property_tpl.substitute({
        "docstring":
        protect_docstring(docstring),
        "property_name":
        property_name,
        "module_name":
        module_name,
        "clj_module_name": py2clojure_function_name(module_name),
        "clj_property_name":
        py2clojure_function_name(property_name)
    })


def get_reference_element(refering_module, full_class_path, class_name):
    return reference_element_tpl.substitute({
        "refering_module": refering_module,
        "full_class_path": full_class_path,
        "class_name": class_name
    })


def get_function(module_name,
                 function_name,
                 positional_args="",
                 kw_args="",
                 defaults="",
                 docstring=""):
    if positional_args and kw_args and defaults:
        return method_positional_kw_defaults.substitute({
            "docstring":
            protect_docstring(docstring),
            "function_name":
            function_name,
            "clj_function_name":
            py2clojure_function_name(function_name),
        "clj_module_name": py2clojure_function_name(module_name),
            "module_name":
            module_name,
            "positional_args":
            positional_args,
            "kw_args":
            kw_args,
            "kw_args_call_format":
            kwargs_to_call_format(kw_args),
            "defaults":
            defaults
        })
    elif positional_args and kw_args:
        return method_positional_kw.substitute({
        "clj_module_name": py2clojure_function_name(module_name),
            "module_name":
            module_name,
            "function_name":
            function_name,
            "clj_function_name":
            py2clojure_function_name(function_name),
            "docstring":
            protect_docstring(docstring),
            "positional_args":
            positional_args,
            "kw_args_call_format":
            kwargs_to_call_format(kw_args),
            "kw_args":
            kw_args
        })
    elif defaults and kw_args:
        return method_kw_defaults.substitute({
        "clj_module_name": py2clojure_function_name(module_name),
            "module_name":
            module_name,
            "function_name":
            function_name,
            "clj_function_name":
            py2clojure_function_name(function_name),
            "docstring":
            protect_docstring(docstring),
            "positional_args":
            positional_args,
            "kw_args":
            kw_args,
            "kw_args_call_format":
            kwargs_to_call_format(kw_args),
            "defaults":
            defaults
        })
    elif kw_args:
        return method_kw.substitute({
        "clj_module_name": py2clojure_function_name(module_name),
            "module_name":
            module_name,
            "function_name":
            function_name,
            "clj_function_name":
            py2clojure_function_name(function_name),
            "docstring":
            protect_docstring(docstring),
            "kw_args_call_format":
            kwargs_to_call_format(kw_args),
            "kw_args":
            kw_args
        })
    elif positional_args:
        return method_positional.substitute({
        "clj_module_name": py2clojure_function_name(module_name),
            "module_name":
            module_name,
            "function_name":
            function_name,
            "clj_function_name":
            py2clojure_function_name(function_name),
            "docstring":
            protect_docstring(docstring),
            "kw_args_call_format":
            kwargs_to_call_format(kw_args),
            "positional_args":
            positional_args
        })
    else:
        return method_positional.substitute({
        "clj_module_name": py2clojure_function_name(module_name),
            "module_name":
            module_name,
            "function_name":
            function_name,
            "clj_function_name":
            py2clojure_function_name(function_name),
            "docstring":
            protect_docstring(docstring),
            "kw_args_call_format":
            kwargs_to_call_format(kw_args),
            "positional_args":
            positional_args
        })

def get_reference_member(member_name,full_class_path):
  return reference_member_tpl.substitute({
        "member_name": py2clojure_function_name(member_name),
        "full_class_path": full_class_path
    })

