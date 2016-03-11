#something
import sys

src_file = ""
des_file = ""

if len(sys.argv) != 3:
    print "Usage python excel_to_req_format.py <src_file> <des_file>"
    sys.exit()


src_file = sys.argv[1]
des_file = sys.argv[2]

if not src_file or not des_file:
    print "Usage python excel_to_req_format.py <src_file> <des_file>"

print "src file "+ src_file +" dest "+des_file

try:
    f = open(src_file,"r")
    g = open(des_file,"w")
except Exception as e:
    print "Some exception "+str(e)
    sys.exit()


f.readline()
f.readline()
f.readline()
sticker_name =""
for line in f:
    data = line.strip("\r\n").split("\t")
    if data[1] != "":
        sticker_name = data[1]
    to_print = "".join([sticker_name, "\t",data[2], "\t",data[3],"\t", data[4],"\t", data[5],"\t",data[7],"\r\n"])
    g.write(to_print)
    print to_print

g.close()
f.close()

