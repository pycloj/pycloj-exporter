"""
Python test file for info.py
"""
import asyncio 
import pandas 

from info import (
  get_class_members,
  get_classes,
  get_submodules,
  get_function_info,
  get_functions, get_function_info)
  


async def test_async(a, b, c=None, d=1):
  pass

def test_dataframe(a, b, c=None, d=pandas.DataFrame()):
  pass




print(get_function_info(test_async))
# this will fail
print(get_function_info(test_dataframe))