from string import Template



method_positional = Template('''
(defn $clj_function_name [ $positional_args ]
  "$docstring"
  (py/call-attr $module_name "$function_name"  $positional_args ))
''')
method_kw = Template('''
(defn $clj_function_name [ & {:keys [$kw_args]} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [] {$kw_args})
''')
 
method_kw_defaults = Template('''
(defn $clj_function_name [ & {:keys [$kw_args]
                          :or {$defaults}} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [] {$kw_args})
''')
method_positional_kw = Template('''
(defn $clj_function_name [$positional_args  & {:keys [$kw_args]} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [$positional_args] {$kw_args})
''')

method_positional_kw_defaults = Template('''
(defn $clj_function_name [$positional_args & {:keys [$kw_args]
                          :or {$defaults} ]
  "$docstring"
   (py/call-attr-kw $module_name "$function_name" [] {$kw_args})
''')
