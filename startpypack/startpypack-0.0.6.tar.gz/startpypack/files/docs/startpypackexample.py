# Import the package
import startpypack

# Set the directory to run the test in
#  (Change this hardcoded directory before testing)
wdir = "/home/vuvlab/Documents"

# Set the name of the new package
pname = "tpp"



# Make a new package
#  (Testing makepackage() function)
startpypack.makepackage(pname,wdir)



# Make a list of 'new function' names
#  (For testing mkfunc() function)
fn = ['newfunc1','newfunc2','newfunc3']

# Add new empty functions to the existing new package
#  (Testing independent use of the mkfunc() function)
for f in fn:
  startpypack.mkfunc(pname=pname, fname=f, wdir=wdir)
