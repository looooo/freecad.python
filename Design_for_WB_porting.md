# Attempt to create new-style modules without adding backward-incompatbilities

### assumption:
1. `<PackageName>` == `<ModuleName>`
2. `<SubModule>` != `<DirectoryName>`

### directories:
1. `Mod/<PackageName>`                      ----> `freecad/<package_name>`
2. `Mod/<PackageName>/<SubPackageName>`     ----> `freecad/<package_name>/<sub_package_name>`

### files:
1. `Mod/<PackageName>/<ModuleName>.py`      ----> `freecad/<package_name>/__init__.py`
2. `Mod/<PackageName>/<SubModuleName>.py`   ----> `freecad/<package_name>/<sub_module_name>.py`
3. `Mod/<PackageName>/Init.py`              ----> `freecad/<package_name>/init.py`
3. `Mod/<PackageName>/InitGui.py`           ----> `freecad/<package_name>/init_gui.py`

### imports (all files in package but no files in submodule)
1. `import <PackageName>`                   ----> `from freecad import <package_name>`
2. `from <PackageName> import <something>`  ----> `from freecad.<package_name> import <something>`

### names (not modules in subpackages)
1. `<PackageName>`                          ----> `<package_name>`
2. `<ModuleName>`                           ----> `<module_name>`   # should be same as names 1. according to assumptioon 1.
3. `<SubModuleName>`                        ----> `<sub_module_name>`
4. `<SubPackageName>`                       ----> `<sub_package_name>`

### backward_compatibility:
1. `Mod/<PackageName>/<ModuleName>.py` replace content with:
```
import warnings
warnings.warn("importing <ModuleName> is deprecated. \n\
               Use 'from freecad import <package_name>' instead", 
               DeprecationWarning)
from freecad.<package_name> import *

```
2. `Mod/<PackageName>/<SubModuleName>.py` replace content with:
```
import warnings
warnings.warn("importing <SubModuleName> is deprecated. \n\
               Use 'from freecad.<package_name> import <sub_module_name>' instead", 
               DeprecationWarning)
from freecad.<package_name>.<sub_module_name> import *
```

3. `Mod/<PackageName>/<SubPackageName>` create new module `Mod/<PackageName>/<SubPackageName>.py`
```
import warnings
warnings.warn("importing <SubPackageName> is deprecated. \n\
               Use 'from freecad.<package_name> import <sub_package_name>' instead", 
               DeprecationWarning)
from freecad.<package_name>.<sub_package_name> import *
```