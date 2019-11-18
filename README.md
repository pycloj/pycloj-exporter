# pycloj-exporter

exporting python modole to be used in clojure with libpython-clj

This project is in an initial stage we expect it to change.

## Usage

Install the python library you intent to export to clojure. 

for example if you wnat to export keras
pip install keras
or 
conda install keras


cd src
python export.py keras

this will generate folders in output/package/pyclj-0.1-keras-THE_KERAS_VERSION

### arguments
to get full argument list  
python export.py -h 

important argument is --sub-modules
if for example you want to export keras but you are only interested in functions and classes under models and layers








## TODO:

### working examples

1. Export library to clojars a 
2. Show how to use it in exampled
3. explain how to use the utility
4. export python tests and use them over clojure
5. replace PyInquirer with sompthing that works on python3.6
6. generate exmple with a test/ exmple project that uses the code
7. handle properties
8 handle ctype class in python see pandas cdef , cclass cimport 
https://github.com/pandas-dev/pandas/blob/master/pandas/_libs/interval.pyx


### bugs to solve
1. files are created twice 



