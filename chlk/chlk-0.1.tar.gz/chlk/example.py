from chalk import chalk


print(chalk.black("test"))
print(chalk.red("test"))
print(chalk.green("test"))
print(chalk.yellow("test"))
print(chalk.blue("test"))
print(chalk.magenta("test"))
print(chalk.cyan("test"))
print(chalk.white("test"))

print(chalk.brightblack("test"))
print(chalk.brightred("test"))
print(chalk.brightgreen("test"))
print(chalk.brightyellow("test"))
print(chalk.brightblue("test"))
print(chalk.brightmagenta("test"))
print(chalk.brightcyan("test"))
print(chalk.brightwhite("test"))

print(chalk.bgblack("test"))
print(chalk.bgred("test"))
print(chalk.bggreen("test"))
print(chalk.bgyellow("test"))
print(chalk.bgblue("test"))
print(chalk.bgmagenta("test"))
print(chalk.bgcyan("test"))
print(chalk.bgwhite("test"))

print(chalk.bgbrightblack("test"))
print(chalk.bgbrightred("test"))
print(chalk.bgbrightgreen("test"))
print(chalk.bgbrightyellow("test"))
print(chalk.bgbrightblue("test"))
print(chalk.bgbrightmagenta("test"))
print(chalk.bgbrightcyan("test"))
print(chalk.bgbrightwhite("test"))

print(chalk.reset("test"))
print(chalk.bold("test"))
print(chalk.dim("test"))
print(chalk.italic("test"))
print(chalk.underline("test"))
print(chalk.inverse("test"))
print(chalk.hidden("test"))
print(chalk.strikethrough("test"))


# below from http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
for i in range(0, 16):
    string = ""
    for j in range(0, 16):
        code = str(i * 16 + j)
        string += chalk.color(str(code).ljust(4), code)
    print(string)


for i in range(0, 16):
    string = ""
    for j in range(0, 16):
        code = str(i * 16 + j)
        string += chalk.bgcolor(str(code).ljust(4), code)
    print(string)





class test:
    def __init__(self):
        self.string =""
