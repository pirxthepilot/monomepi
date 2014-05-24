import ledfont

t = "h"
d = ledfont.ledmap(ord(t))

for line in d:
    #print format(line, "02x")
    print format(line, "08b")
