from string import Template

project_tpl = Template('''
(defproject $project "$version"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.0"] [libpython-clj "1.6-SNAPSHOT"][alembic "0.3.2"]]
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
''')
