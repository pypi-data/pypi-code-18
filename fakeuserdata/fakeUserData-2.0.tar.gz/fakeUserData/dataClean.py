# Read in the file
name = 'femaleNames'


f=open(name+'.txt',"r")
lines=f.read().split(',')
f.close()
with open(name+'.txt', 'w') as file:
	for x in range(0,len(lines)):
		# if "'" in lines[x]:
		# 	print(x)
		file.write(lines[x])
		file.write("\n")
		file.write(',')



# with open(name+'.txt', 'r') as file :
#   filedata = file.read()

# # Replace the target string
# filedata = filedata.replace("'",'')

# # Write the file out again
# with open(name+'.txt', 'w') as file:
#   file.write(filedata)


