__author__ = 'patley'

f = open("/Users/patley/Downloads/stickers_list.txt","r")
g = open("stickers_list.csv","w")
h = open("stickers_cat.txt",'w')

category = ""
new_cat = False
for line in f:
    data = line.strip("\r\n").split(" ")

    if len(data) ==2:
        category = data[1]
        new_cat = True
    elif len(data) ==3:
        if new_cat:
            new_cat = False
            h.write("".join([category,",",data[2],"\n"]))
        g.write("".join([category,",",data[2],"\n"]))
    else:
        pass

h.close()
g.close()
f.close()
