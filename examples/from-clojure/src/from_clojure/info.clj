(ns from-clojure.info
  (:require [libpython-clj.python :as py]
            [libpython-clj.require :refer [require-python]]
            [clojure.string :as string]))

(require-python '([builtins :as python]
                  argparse
                  inspect
                  pkgutil
                  operator))

(defn protect-doctstring [dstr]
  (if (string? dstr)
    (string/replace dstr "\"" "\\\"")))

(defn module->name [module]
  (when-not (:failed-import? module)
    (py/get-attr module "__name__")))

(def name->module
  (memoize
   (fn [module-name]
     (try (py/import-module module-name)
          (catch Exception e
            {:failed-import? true
             :module-name   module-name})))))

(comment
  (name->module "pandas")
;; => <module 'pandas' from '/home/daslu/.local/lib/python3.6/site-packages/pandas/__init__.py'>

  (-> "pandas"
      name->module
      module->name)
;; => "pandas"

  (name->module "pandas.compat.numpy.compat")
;; =>
 {:failed-import? true, :module-name "pandas.compat.numpy.compat"}
)

(defn module->submodules-names [module]
  (when-not (:failed-import? module)
    (->> (py/get-attr module "__path__")
         (pkgutil/walk_packages :path)
         (map py/->jvm)
         (filter (fn [[_ _ ispkg]]
                   ispkg))
         (map (fn [[_ m _]]
                (-> module
                    module->name
                    (str "." m)))))))

(comment
  (-> "pandas"
      name->module
      module->submodules-names)
  ;; => 
  ("pandas._config" "pandas._libs" "pandas.api" "pandas.arrays" "pandas.compat" "pandas.core" "pandas.errors" "pandas.io" "pandas.plotting" "pandas.tests" "pandas.tseries" "pandas.util")

  (-> "pandas.compat.numpy"
      name->module
      module->submodules-names)
  ;; => ()

  (-> "pandas.compat.numpy.compat"
      name->module ; failed import
      module->submodules-names)
  ;; => nil
  )

(defn module->submodules [module]
  (->> module
       module->submodules-names
       (map name->module)))

(comment
  (->> "pandas"
       name->module
       module->submodules
       (map module->name))
;; =>
 ("pandas._config" "pandas._libs" "pandas.api" "pandas.arrays" "pandas.compat" "pandas.core" "pandas.errors" "pandas.io" "pandas.plotting" "pandas.tests" "pandas.tseries" "pandas.util")
  )

(defn module->recursive-submodules [module]
  (->> module
       module->submodules
       (mapcat module->recursive-submodules)
       (cons module)))

(comment
  (->> "pandas"
       name->module
       module->recursive-submodules
       (filter :failed-import?)
       (map :module-name))
  ;; =>
  ("pandas.compat.numpy.compat" "pandas.compat.numpy.compat.tests" "pandas.compat.numpy.core" "pandas.compat.numpy.core.tests" "pandas.compat.numpy.distutils" "pandas.compat.numpy.distutils.command" "pandas.compat.numpy.distutils.fcompiler" "pandas.compat.numpy.distutils.tests" "pandas.compat.numpy.doc" "pandas.compat.numpy.f2py" "pandas.compat.numpy.f2py.tests" "pandas.compat.numpy.fft" "pandas.compat.numpy.fft.tests" "pandas.compat.numpy.lib" "pandas.compat.numpy.lib.tests" "pandas.compat.numpy.linalg" "pandas.compat.numpy.linalg.tests" "pandas.compat.numpy.ma" "pandas.compat.numpy.ma.tests" "pandas.compat.numpy.matrixlib" "pandas.compat.numpy.matrixlib.tests" "pandas.compat.numpy.polynomial" "pandas.compat.numpy.polynomial.tests" "pandas.compat.numpy.random" "pandas.compat.numpy.random.tests" "pandas.compat.numpy.random.tests.data" "pandas.compat.numpy.testing" "pandas.compat.numpy.testing._private" "pandas.compat.numpy.testing.tests" "pandas.compat.numpy.tests" "pandas.tests.extension.base")

  (->> "pandas"
       name->module
       module->recursive-submodules
       (filter (complement :failed-import?))
       (map module->name))
  ;; =>
  ("pandas" "pandas._config" "pandas._libs" "pandas._libs.tslibs" "pandas.api" "pandas.api.extensions" "pandas.api.types" "pandas.arrays" "pandas.compat" "pandas.compat.numpy" "pandas.core" "pandas.core.arrays" "pandas.core.computation" "pandas.core.dtypes" "pandas.core.groupby" "pandas.core.indexes" "pandas.core.internals" "pandas.core.ops" "pandas.core.reshape" "pandas.core.sparse" "pandas.core.tools" "pandas.core.util" "pandas.errors" "pandas.io" "pandas.io.clipboard" "pandas.io.excel" "pandas.io.formats" "pandas.io.json" "pandas.io.msgpack" "pandas.io.sas" "pandas.plotting" "pandas.plotting._matplotlib" "pandas.tests" "pandas.tests.api" "pandas.tests.arithmetic" "pandas.tests.arrays" "pandas.tests.arrays.categorical" "pandas.tests.arrays.interval" "pandas.tests.arrays.sparse" "pandas.tests.computation" "pandas.tests.config" "pandas.tests.dtypes" "pandas.tests.dtypes.cast" "pandas.tests.extension" "pandas.tests.extension.arrow" "pandas.tests.extension.decimal" "pandas.tests.extension.json" "pandas.tests.extension.list" "pandas.tests.extension.numpy_" "pandas.tests.frame" "pandas.tests.generic" "pandas.tests.groupby" "pandas.tests.groupby.aggregate" "pandas.tests.indexes" "pandas.tests.indexes.datetimes" "pandas.tests.indexes.interval" "pandas.tests.indexes.multi" "pandas.tests.indexes.period" "pandas.tests.indexes.timedeltas" "pandas.tests.indexing" "pandas.tests.indexing.interval" "pandas.tests.indexing.multiindex" "pandas.tests.internals" "pandas.tests.io" "pandas.tests.io.excel" "pandas.tests.io.formats" "pandas.tests.io.json" "pandas.tests.io.msgpack" "pandas.tests.io.parser" "pandas.tests.io.pytables" "pandas.tests.io.sas" "pandas.tests.plotting" "pandas.tests.reductions" "pandas.tests.resample" "pandas.tests.reshape" "pandas.tests.reshape.merge" "pandas.tests.scalar" "pandas.tests.scalar.interval" "pandas.tests.scalar.period" "pandas.tests.scalar.timedelta" "pandas.tests.scalar.timestamp" "pandas.tests.series" "pandas.tests.series.indexing" "pandas.tests.sparse" "pandas.tests.sparse.frame" "pandas.tests.sparse.series" "pandas.tests.tools" "pandas.tests.tseries" "pandas.tests.tseries.frequencies" "pandas.tests.tseries.holiday" "pandas.tests.tseries.offsets" "pandas.tests.tslibs" "pandas.tests.util" "pandas.tests.window" "pandas.tseries" "pandas.util")
)


(defn empty->nil [v]
  (when-not (operator/eq inspect/_empty v)
    v))

(defn module->functions-map [module]
  (->> module
       inspect/getmembers
       (filter (fn [[k v]]
                 (inspect/isfunction v)))
       (map (fn [[k v]]
              [(keyword k) (empty->nil v)]))
       (into {})))

(comment
  (->> "pandas"
       name->module
       module->functions-map)
;; => {:to_timedelta <function to_timedelta at 0x7fd7bee338c8>, :merge_ordered <function merge_ordered at 0x7fd7bca8a8c8>, :read_feather <function read_feather at 0x7fd7bc76d7b8>, :unique <function unique at 0x7fd7bfab3a60>, :timedelta_range <function timedelta_range at 0x7fd7bedbc730>, :read_spss <function read_spss at 0x7fd7bc522c80>, :read_msgpack <function read_msgpack at 0x7fd7bc525048>, :to_msgpack <function to_msgpack at 0x7fd7bc505ae8>, :read_csv <function _make_parser_function.<locals>.parser_f at 0x7fd7bca479d8>, :read_fwf <function read_fwf at 0x7fd7bca47ae8>, :to_datetime <function to_datetime at 0x7fd7bfa00048>, :read_sql_table <function read_sql_table at 0x7fd7bbc55bf8>, :set_eng_float_format <function set_eng_float_format at 0x7fd7be634a60>, :read_html <function read_html at 0x7fd7bc786730>, :notnull <function notna at 0x7fd7c01ccf28>, :factorize <function factorize at 0x7fd7bfab3d08>, :concat <function concat at 0x7fd7bca83a60>, :read_json <function read_json at 0x7fd7bc505510>, :infer_freq <function infer_freq at 0x7fd7bfa18730>, :qcut <function qcut at 0x7fd7bca248c8>, :read_table <function _make_parser_function.<locals>.parser_f at 0x7fd7bca47a60>, :read_sas <function read_sas at 0x7fd7bbc55620>, :read_sql <function read_sql at 0x7fd7bbc55d08>, :interval_range <function interval_range at 0x7fd7bedc0950>, :lreshape <function lreshape at 0x7fd7bca8a158>, :array <function array at 0x7fd7c1141598>, :read_stata <function read_stata at 0x7fd7bbbe6a60>, :merge <function merge at 0x7fd7bca8a7b8>, :period_range <function period_range at 0x7fd7bed529d8>, :merge_asof <function merge_asof at 0x7fd7bca8a950>, :notna <function notna at 0x7fd7c01ccf28>, :isnull <function isna at 0x7fd7c01ccbf8>, :read_parquet <function read_parquet at 0x7fd7bc525d90>, :to_numeric <function to_numeric at 0x7fd7bfa202f0>, :date_range <function date_range at 0x7fd7bededbf8>, :wide_to_long <function wide_to_long at 0x7fd7bca8a1e0>, :show_versions <function show_versions at 0x7fd7bca24f28>, :read_sql_query <function read_sql_query at 0x7fd7bbc55c80>, :melt <function melt at 0x7fd7bca8a0d0>, :read_hdf <function read_hdf at 0x7fd7bbc3e6a8>, :pivot <function pivot at 0x7fd7bca24488>, :isna <function isna at 0x7fd7c01ccbf8>, :value_counts <function value_counts at 0x7fd7bfab3bf8>, :read_pickle <function read_pickle at 0x7fd7bc5221e0>, :bdate_range <function bdate_range at 0x7fd7bededc80>, :read_gbq <function read_gbq at 0x7fd7bc76da60>, :crosstab <function crosstab at 0x7fd7bca24510>, :pivot_table <function pivot_table at 0x7fd7bca24048>, :get_dummies <function get_dummies at 0x7fd7bcd3f488>, :read_clipboard <function read_clipboard at 0x7fd7bca29268>, :test <function test at 0x7fd7bca29158>, :to_pickle <function to_pickle at 0x7fd7bc525e18>, :cut <function cut at 0x7fd7bca24840>, :read_excel <function read_excel at 0x7fd7bc7589d8>, :eval <function eval at 0x7fd7bca838c8>}
  )

(defn module->classes [module]
  (->> module
       inspect/getmembers
       (filter (fn [[k v]]
                 (inspect/isclass v)))
       (map (fn [[k v]]
              [(keyword k) (empty->nil v)]))
       (into {})))

(comment
  (->> "pandas"
       name->module
       module->classes)
  ;; If you try to print it, an error occurs.
  ;; See discussion here: https://clojurians.zulipchat.com/#narrow/stream/215609-libpython-clj-dev/topic/some.20things.20cannot.20be.20printed
  )

(defn function->info [f]
  (let [sig  (inspect/signature f)
             args (-> sig
                      (py/get-attr "parameters")
                      (py/call-attr "values")
                      (->>
                       (mapv (fn [arg]
                               (-> (->> [:name :empty :kind :default :annotation]
                                        (map (fn [k]
                                               [k (->> k
                                                       (py/get-attr arg)
                                                       empty->nil)]))
                                        (into {}))
                                   (update :kind (comp keyword python/str)))))))]
         {:name              (py/get-attr f "__name__")
          :args              args
          :return-annotation (-> sig
                                 (py/get-attr "return_annotation")
                                 empty->nil)
          :doc               (protect-doctstring
                              (py/get-attr f "__doc__"))
          :generator?        (inspect/isgeneratorfunction f)
          :async?            (inspect/iscoroutine f)
          :awaitable?        (inspect/isawaitable f)
          :builtin?          (inspect/isbuiltin f)}))

(comment
  (-> "pandas"
      name->module
      module->functions-map
      :isna
      function->info)
  ;; =>
  {:name              "isna",
     :args
     [{:name       "obj",
       :empty      nil,
       :kind       :POSITIONAL_OR_KEYWORD,
       :default    nil,
       :annotation nil}],
     :return-annotation nil,
     :doc
     "\n    Detect missing values for an array-like object.\n\n    This function takes a scalar or array-like object and indicates\n    whether values are missing (``NaN`` in numeric arrays, ``None`` or ``NaN``\n    in object arrays, ``NaT`` in datetimelike).\n\n    Parameters\n    ----------\n    obj : scalar or array-like\n        Object to check for null or missing values.\n\n    Returns\n    -------\n    bool or array-like of bool\n        For scalar input, returns a scalar boolean.\n        For array input, returns an array of boolean indicating whether each\n        corresponding element is missing.\n\n    See Also\n    --------\n    notna : Boolean inverse of pandas.isna.\n    Series.isna : Detect missing values in a Series.\n    DataFrame.isna : Detect missing values in a DataFrame.\n    Index.isna : Detect missing values in an Index.\n\n    Examples\n    --------\n    Scalar arguments (including strings) result in a scalar boolean.\n\n    >>> pd.isna('dog')\n    False\n\n    >>> pd.isna(np.nan)\n    True\n\n    ndarrays result in an ndarray of booleans.\n\n    >>> array = np.array([[1, np.nan, 3], [4, 5, np.nan]])\n    >>> array\n    array([[ 1., nan,  3.],\n           [ 4.,  5., nan]])\n    >>> pd.isna(array)\n    array([[False,  True, False],\n           [False, False,  True]])\n\n    For indexes, an ndarray of booleans is returned.\n\n    >>> index = pd.DatetimeIndex([\\\"2017-07-05\\\", \\\"2017-07-06\\\", None,\n    ...                           \\\"2017-07-08\\\"])\n    >>> index\n    DatetimeIndex(['2017-07-05', '2017-07-06', 'NaT', '2017-07-08'],\n                  dtype='datetime64[ns]', freq=None)\n    >>> pd.isna(index)\n    array([False, False,  True, False])\n\n    For Series and DataFrame, the same type is returned, containing booleans.\n\n    >>> df = pd.DataFrame([['ant', 'bee', 'cat'], ['dog', None, 'fly']])\n    >>> df\n         0     1    2\n    0  ant   bee  cat\n    1  dog  None  fly\n    >>> pd.isna(df)\n           0      1      2\n    0  False  False  False\n    1  False   True  False\n\n    >>> pd.isna(df[1])\n    0    False\n    1     True\n    Name: 1, dtype: bool\n    ",
     :generator?        false,
     :async?            false,
     :awaitable?        false,
     :builtin?          false}
)


