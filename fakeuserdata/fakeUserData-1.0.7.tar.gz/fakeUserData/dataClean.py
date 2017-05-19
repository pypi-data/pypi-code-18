# Read in the file
name = 'streetSuffixes'


f=open(name+'.txt',"r")
lines=f.readlines()
f.close()
import random
with open(name+'.txt', 'w') as file:
	for x in lines:
		file.write(x)
		file.write(',')



with open(name+'.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('\n','')

# Write the file out again
with open(name+'.txt', 'w') as file:
  file.write(filedata)


