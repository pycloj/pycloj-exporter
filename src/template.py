from string import Template
module_head = Template('''
(ns $ns
  ""
  (:require [libpython-clj.python
             :refer [import-module
                     get-item
                     get-attr
                     python-type
                     call-attr
                     call-attr-kw
                     att-type-map
                     ->py-dict
                     ->py-list
                     ]
             :as py]
            [clojure.pprint :as pp]))

(py/initialize!)
(defonce $module_name (import-module "$module_name"))
''')

method_positional = Template('''
(defn $function_name [ $positional_args ]
  "$docstring"
  (py/call-attr $module_name "$function_name"  $positional_args ))
''')
method_kw = Template('''
(defn $function_name [ & {:keys [$kw_args]} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [] {$kw_args})
''')
 
method_kw_defaults = Template('''
(defn $function_name [ & {:keys [$kw_args]
                          :or {$defaults}} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [] {$kw_args})
''')
method_positional_kw = Template('''
(defn $function_name [$positional_args  & {:keys [$kw_args]} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [$positional_args] {$kw_args})
''')

method_positional_kw_defaults = Template('''
(defn $function_name [$positional_args & {:keys [$kw_args]
                          :or {$defaults} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [] {$kw_args})
''')



def get_module_head(namespace, module_name):
  return module_head.substitute({"namespace":namespace, "module_name":module_name})

def get_function(module_name, positional_args=None, kw_args=None, defaults=None, docstring=""):
  if positional_args and kw_args and defaults:
    return method_positional_kw_defaults.replace({
      "positional_args":positional_args,
      "kw_args":kw_args,
      "defaults":defaults
    })
  elif positional_args and kw_args:
    return method_positional_kw.replace({
      "positional_args":positional_args,
      "kw_args":kw_args
    })
  elif  defaults and kw_args:
    return method_kw_defaults.replace({
      "positional_args":positional_args,
      "kw_args":kw_args
    })
  elif kw_args:
    return method_kw.replace({
      "kw_args":kw_args
    })
  elif positional_args:
    return method_positional.replace({
      "positional_args":positional_args
    })

