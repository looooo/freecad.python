from setuptools import setup
import os
import jinja2
import subprocess as sub
# This setup needs FreeCAD to be available!

proc = sub.Popen(['FreeCAD', '-c', "import os; import FreeCADGui; print(os.path.dirname(FreeCADGui.__file__))"], stdout=sub.PIPE, stderr=sub.PIPE)
out, err = proc.communicate()
if err:
    raise(RuntimeError(err.decode("utf-8")))
output = out.decode("utf-8")
freecad_lib_path = output.split("\n")[0].rstrip()

print("\n\n##############################")
print("path to the freecad library is: \n")
print(freecad_lib_path)
print("##############################\n\n")

template_dir = os.path.join(os.path.dirname(__file__), "freecad")
template_fn = os.path.join(template_dir, "__init__.py.template")
render_fn = os.path.join(template_dir, "__init__.py")
with open(template_fn, "r") as template_file:
    template_content = template_file.read()
    template = jinja2.Template(template_content)
    output = template.render(PATH_TO_FREECAD=str(freecad_lib_path))
    with open(render_fn, "w") as render_file:
        render_file.write(output)


setup(name='freecad.python',
      version="0.0.1",
      packages=['freecad'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/FreeCAD/freecad.python",
      description="a package to make freecad directly accessable via python",
      include_package_data=True)
