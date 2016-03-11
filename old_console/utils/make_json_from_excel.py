__author__ = 'patley'


lang_doc = {}
doc = {'*cgeneral': [], '*cother': [], '*csmiley': [], 'catId': 'lovequotes', 'sIds': '002_lq_myhero.png', '*cbehaviour': [], '*afestival': [], '*cfeeling': [], '*cresponse': [], '*atime': -1, '*cemotion': [], '*creaction': [], '*ctheme': []}


#vi /Users/patley/development/hyderabad_tsv.txt
f = open("/Users/patley/development/hyderabad_tsv.txt","r")
print f.readline()
li = ['theme','reaction','behaviour','emotion','feeling']
sticker_name = ""
#doc[]

for line in f:
    print line.strip("\n")
    data = line.lower().strip("\n").split("\t")
    if data[1] != sticker_name:
        sticker_name = data[1]
        stick = {}
        stick[data[7]] = {'*cgeneral': [], '*cother': [], '*csmiley': [], 'catId': 'hyderabad', 'sIds': data[1]+".png", '*cbehaviour': [], '*afestival': [], '*cfeeling': [], '*cresponse': [], '*atime': -1, '*cemotion': [], '*creaction': [], '*ctheme': []}
        count =0
        for item in data[2:6]:

            if item is not None:
                count += 1
                print item, " ",count
