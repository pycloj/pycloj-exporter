from string import Template
reference_element_tpl = Template('''
(ns $refering_module
  (:require [$full_class_path]))

(defonce $class_name $full_class_path/$class_name)

''')


