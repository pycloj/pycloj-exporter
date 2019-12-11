(ns from-clojure.core
  (:require [libpython-clj.python :as py]
            [libpython-clj.require :refer [require-python]]))


(require-python '[info :reload])

(info/import_module "keras")

