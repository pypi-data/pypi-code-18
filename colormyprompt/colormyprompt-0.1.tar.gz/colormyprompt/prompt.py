import sys
colors ={
"RED": "\033[1;31m",
"BLUE"  : "\033[1;34m",
"CYAN"  : "\033[1;36m",
"GREEN" : "\033[0;32m",
"RESET" : "\033[0;0m",
"BOLD"    : "\033[;1m",
"REVERSE" : "\033[;7m"
}

def colorprint(msgs="", clr="RESET"):
        clr = "RESET" if clr not in colors else clr
        sys.stdout.write(colors[clr])
        if isinstance(msgs, list):
            for m in msgs:
                print(m)
        elif isinstance(msgs, str):
            print(msgs)
        sys.stdout.write(colors["RESET"])
