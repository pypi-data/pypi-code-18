import os

# Remove previous build results
os.system("rm -R build")
os.system("rm -R dist")
os.system("rm -R *egg-info")

os.system("python setup.py sdist")
os.system("python setup.py bdist_wheel --universal")
