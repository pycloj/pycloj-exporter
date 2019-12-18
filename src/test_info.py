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
  get_functions, get_function_info,
  get_class_members)
  


async def test_async(a, b, c=None, d=1):
  pass

def test_dataframe(a, b, c=(1,2,3), d=pandas.DataFrame()):
  pass


class TestClassBase(object):
  #class members
  __test1=0
  __test2=1
  def __init__(self, a, b=None, c=(1,2,3)):
    self.a = a
    self.b = b
    self.c = c

  def __repr__(self):
    return super().__repr__()

  def show(self):
    print(self.a, self.b, self.c)

class TestClassSub(TestClassBase):
  def __init__(self, a, b=None, c=(1,2,3)):
    super().__init__(TestClassSub, a,b,c)







print(get_function_info(test_async))
# this will fail
print(get_function_info(test_dataframe))


print(get_class_members(TestClassBase))