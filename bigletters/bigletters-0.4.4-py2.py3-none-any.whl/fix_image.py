from PIL import Image
carte = Image.open('bigletters/abcd.png').convert('RGB')
print "carte = ["
for y in range(0, carte.height):
    row = ""
    for x in range(0, carte.width):
        pix, _, _ = carte.getpixel((x, y))
        row += "X" if pix < 1 else " "
    print '\t"{}"{}'.format(row, ',' if y < carte.height -1 else '')
print "]"
