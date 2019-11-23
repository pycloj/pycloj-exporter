from distutils.dir_util import mkpath
import os
from version import VERSION

def save_file(src_path, path, filename, data):
  mkpath(os.path.join(src_path,path))
  with open(os.path.join(src_path, path, filename), "w") as f:
    for l in data:
      f.writelines(l)

def make_src_path(base_path, module_name, version):
  path = os.path.join(base_path, module_name,
                        f"pyclj-{VERSION}-{module_name}{version}")
  if os.path.exists(path):
    for i in range(50):
        try:
            os.rename(path, f"{path}__{i}")
            break
        except:
            pass
  # print(base_path, module_name, version)
  # print(path)
  project_path = mkpath(path)[0]
  print(project_path)
  src_path = mkpath(os.path.join(project_path,"src"))[0]
  print(project_path, src_path)
  # exit(0)
  return project_path, src_path
