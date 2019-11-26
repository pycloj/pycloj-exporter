from string import Template



method_no_args = Template("""
(defn $clj_function_name 
  "$docstring"
  [  ]
  (py/call-attr $clj_module_name "$function_name"  ))
""")

method_positional = Template("""
(defn $clj_function_name 
  "$docstring"
  [ $positional_args ]
  (py/call-attr $clj_module_name "$function_name"  $positional_args ))
""")
method_kw = Template("""
(defn $clj_function_name 
  "$docstring"
  [ & {:keys [$kw_args]} ]
   (py/call-attr-kw $clj_module_name "$function_name" [] {$kw_args_call_format}))
""")
 
method_kw_defaults = Template("""
(defn $clj_function_name 
  "$docstring"
  [ & {:keys [$kw_args]
       :or {$defaults}} ]
  
   (py/call-attr-kw $clj_module_name "$function_name" [] {$kw_args_call_format}))
""")
method_positional_kw = Template("""(defn $clj_function_name 
  "$docstring"
  [$positional_args  & {:keys [$kw_args]} ]
    (py/call-attr-kw $clj_module_name "$function_name" [$positional_args_call_format] {$kw_args_call_format}))
""")

method_all_tpl = Template("""
(defn $clj_function_name 
  "$docstring"
  [$positional_args & {:keys [$kw_args]
                       :or {$defaults}} ]
    (py/call-attr-kw $clj_module_name "$function_name" [$positional_args_call_format] {$kw_args_call_format}))
""")

method_all_defaults_tpl = Template("""
(defn $clj_function_name 
  "$docstring"
  [$positional_args & {:keys [$kw_args]} ]
    (py/call-attr-kw $clj_module_name "$function_name" [$positional_args_call_format] {$kw_args_call_format}))
""")


method_positional_kw_defaults = Template("""
(defn $clj_function_name 
  "$docstring"
  [$positional_args & {:keys [$kw_args]
                       :or {$defaults}} ]
    (py/call-attr-kw $clj_module_name "$function_name" [$positional_args_call_format] {$kw_args_call_format}))
""")



property_tpl = Template("""
(defn $clj_property_name 
  "$docstring"
  [ self ]
    (py/call-attr self "$property_name"))
""")
