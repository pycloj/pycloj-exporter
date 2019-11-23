import keras


def get_element_location(element, module):
  print(module.__name__, element.__name__) 

  

get_element_location(keras.Input, keras)
get_element_location(keras.Model, keras)
get_element_location(keras.Sequential, keras)
get_element_location(keras.layers.Dense, keras.layers)

    
  
  
