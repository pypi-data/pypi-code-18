from bigletters.carte import carte
import sys

def main():
    text = ""
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        import easygui
        text = easygui.enterbox("type something.")
    text = text.upper()
    cache = [""] * 10
    order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for letter in text:
        i = 0
        try:
            i = order.index(letter)
        except ValueError:
            raise
            i = order.index(' ')
        j = (i//6)*10
        i = (i%6)*10
        for y in range(j, j+10):
            row = ""
            for x in range(i, i+10):
                pix = carte[y][x]
                row += letter if pix == "X" else " "
            cache[y - j] += row

    for line in cache:
        print(line)

if __name__ == "__main__":
    main()
