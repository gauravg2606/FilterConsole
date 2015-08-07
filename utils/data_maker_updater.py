__author__ = 'patley'


BASE_URL  = "/Users/patley/hello/stickers/"
f = open(BASE_URL+"lovequotes.txt","r")
g = open(BASE_URL+"lovequotes_pack_stk_packs_list.csv","w")
h = open(BASE_URL+"lovequotes_pack_sticker_stk_packs_cat.txt",'w')

category = ""
new_cat = False
for line in f:

    data = line.strip("\r\n").split(" ")
    print data
    # print len(data)
    # print line
    # print data
    if len(data) ==2:
        category = data[1]
        print "category"+str(category)
        new_cat = True
    elif len(data) >= 3:
        if new_cat:
            new_cat = False
            h.write("".join([category,",",data[-1],"\n"]))
        g.write("".join([category,",",data[-1],"\n"]))
    else:
        pass

h.close()
g.close()
f.close()
