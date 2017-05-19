# Read in the file
name = 'domains'


f=open(name+'.txt',"r")
lines=f.read().split(',')
f.close()
with open(name+'.txt', 'w') as file:
	for x in lines:
		file.write("'")
		file.write(x)
		file.write("'")
		file.write(',')



# with open(name+'.txt', 'r') as file :
#   filedata = file.read()

# # Replace the target string
# filedata = filedata.replace('\n',',')

# # Write the file out again
# with open(name+'.txt', 'w') as file:
#   file.write(filedata)


