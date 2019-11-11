import os, sys
import shutil
import glob
import re

def camel2snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def recursive_mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def port_new_style(in_dir, out_dir, PackageName, package_name=None, Prefix=None):
    package_name = package_name or camel2snake(PackageName)
    Prefix = Prefix or PackageName

    # 1 copy all files from in_dir/PackageName to out_dir/freecad/package_name:

    PackageDir = os.path.join(in_dir, PackageName)
    package_dir = os.path.join(out_dir, "freecad", package_name)
    shutil.rmtree(package_dir, True)
    recursive_mkdir(package_dir)
    Files = glob.glob(os.path.join(PackageDir, "*.py"))
    Files = [f for f in Files if not "rc" in f]
    for Fn in Files:
        shutil.copy2(Fn, package_dir)
    # TODO: same for directories aka subpackages

    # 2 crete name dict:
    FileBasenames = list(map(os.path.basename, Files))

    module_dict = {}
    for Fn in FileBasenames:
        if Fn == PackageName + ".py":
            fn = "__init__.py"
        else:
            fn = Fn.replace(PackageName, "")  # replacing prefix
            fn = camel2snake(fn)
        module_dict[Fn] = fn
    # TODO: same for directories aka subpackages (but only one layer)

    # 3 rename copied files:
    for Fn, fn in module_dict.items():
        os.rename(os.path.join(package_dir, Fn), os.path.join(package_dir, fn))
    
    # 4: backward compatibility:    
    
    reworkedPackageDir = PackageDir + "_reworked"
    shutil.rmtree( reworkedPackageDir, True)
    shutil.copytree(PackageDir, reworkedPackageDir)
    
    import_package = """
import warnings
warnings.warn("importing {package} is deprecated. Use 'from freecad import {package}' instead", DeprecationWarning)
from freecad.{package} import *"""
    import_module = """
import warnings
warnings.warn("importing {module} is deprecated. Use 'from freecad.{package} import {module}' instead", DeprecationWarning)
from freecad.{package}.{module} import *"""


    import_submodule = """
from freecad.{package}.{module} import *"""
    for Fn in FileBasenames:
        with open(os.path.join(reworkedPackageDir, Fn), "w") as b_file:
            if Fn == PackageName + ".py":
                b_file.write(import_package.format(package=package_name))
            else:
                b_file.write(import_module.format(package=package_name, module=os.path.splitext(module_dict[Fn])[0]))

# remove Init.py
# remove InitGui.py