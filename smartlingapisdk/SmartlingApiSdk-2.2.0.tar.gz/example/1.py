f = open("../resources/java.properties", "rb"); d = f.read(); f.close()


f = open("../resources/java.properties2", "wb"); 

ls = d.split("4")
f.write(ls[0])
f.write(chr(0xc4))
f.write(chr(0x84))
f.write(ls[1])
f.close()
