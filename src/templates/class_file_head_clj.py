from string import Template
class_file_head = Template('''(ns $module_name_clj.$class_name_clj
  "$docstring"
  (:require [libpython-clj.python
             :refer [import-module
                     get-item
                     get-attr
                     python-type
                     call-attr
                     call-attr-kw]:as py]))

(py/initialize!)
(defonce $last_module_part_clj (import-module "$module_name"))
''')
