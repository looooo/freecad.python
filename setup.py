from setuptools import setup
import os
import shutil
import jinja2
import subprocess as sub
# This setup needs FreeCAD to be available!

cmd = "FreeCAD"
if not shutil.which(cmd):  # restricted to python_version > 3.3
    cmd = "freecad"

# we need to find a reliable method to get the path to the freecad library!!!
# best to define a "freecad --get_lib_dir"

path_to_freecad_libdir = None
try:
    path_to_freecad_libdir = os.environ["PATH_TO_FREECAD_LIBDIR"]
except KeyError:
    print("try to find FreeCAD by calling the programmm")
    proc = sub.Popen([cmd, '-c', "import os; import FreeCADGui; print(os.path.dirname(FreeCADGui.__file__))"], 
        stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = proc.communicate()
    if err:
        raise(RuntimeError(err.decode("utf-8")))
    output = out.decode("utf-8")
    for line in output.split():
        if os.path.exists(line):
            path_to_freecad_libdir = line
            break
    else:
        raise RuntimeError("cannot find FreeCAD-library-dir. \
Please specify with environment-variable: PATH_TO_FREECAD_LIBDIR")
        

print("\n\n##############################")
print("path to the freecad library is: \n")
print(path_to_freecad_libdir)
print("##############################\n\n")

template_dir = os.path.join(os.path.dirname(__file__), "freecad")
template_fn = os.path.join(template_dir, "__init__.py.template")
render_fn = os.path.join(template_dir, "__init__.py")
with open(template_fn, "r") as template_file:
    template_content = template_file.read()
    template = jinja2.Template(template_content)
    output = template.render(PATH_TO_FREECAD_LIBDIR=str(path_to_freecad_libdir))
    with open(render_fn, "w") as render_file:
        render_file.write(output)



setup(name='freecad.python',
      version="0.0.1",
      packages=['freecad'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/FreeCAD/freecad.python",
      description="a package to make freecad directly accessible via python",
      include_package_data=True)
