##Gen imports
import datetime
## Django imports
from django.db import models
from django.utils import timezone
import json
# Create your models here.

tagthem = {"*ctheme":"theme","*cemotion":"emotion","*cfeeling":"feeling","*cbehaviour":"behaviour","*creaction":"reaction","*csmiley":"smiley","*cresponse":"response","*cgeneral":"general","*cother":"other","*ctitle":"title"}
tagthem_inv = {"theme":"*ctheme","emotion":"*cemotion","feeling":"*cfeeling","behaviour":"*cbehaviour","reaction":"*creaction","smiley":"*csmiley","response":"*cresponse","general":"*cgeneral","other":"*cother","title":"*ctitle"}
tagstarter = {"*ctheme":[],"*cemotion":[],"*cfeeling":[],"*cbehaviour":[],"*creaction":[],"*csmiley":[],"*cresponse":[],"*cgeneral":[],"*cother":[],"*ctitle":[]}
langconv = {"english":"eng","hindi":"hin","marathi":"mar","hinglish":"hin","assamese":"asm","awadhi":"awa","bengali":"ben","bhojpuri":"bho","bundeli":"bns","chattisgarhi":"hne","dogri":"doi","garhwali":"gbm","gujarati":"guj","haryanvi":"bgc","hyderabadi":"dcc","kangri":"xnr","kannada":"kan","kashmiri":"kas","khariboli":"59-AAF-qd","kortha":"east2315","konkani":"kok","malayalam":"mal","malvi":"mup","oriya":"ori","punjabi":"pan","rajasthani":"raj","tamil":"tam","telugu":"tel","tulu":"tcy","urdu":"urd","garo":"grt","khasi":"kha","mizo":"lus","manipuri":"mni","kok borok":"trp","sikkim":"sip","nepali":"nep","bodo":"brx","lepcha":"lep","sindhi":"snd","nagamese":"nag","kumaoni":"kfy","maithili":"mai"}

### General function
def get_names_of_list(list_to):
    """
    Assumes there is a name attribute to whatwever is being passed
    :param list_to: list of objects having name attribute
    :return:
    """
    return [tg.name for tg in list_to]


def search_for(term):
    return Sticker.objects.filter(name__icontains=term)


class Category(models.Model):
    name= models.CharField(max_length=25)
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date added',auto_now_add=True, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes= models.IntegerField(default=0)
    banner = models.CharField(max_length=150,default=None)

    def __str__(self):
        return self.name
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_json(category):
        for stick in Sticker.objects.filter(category=category):
            print stick.make_str_json()
            print "\n"
        return

    @staticmethod
    def get_category_json_lang(cat,languages_list):
        print "get_category_json_lang (" + cat
        new_str = ""
        json_list = []
        for stick in Sticker.objects.filter(category=str(cat)):
            for langu in languages_list:
                temp =  stick.get_lang_dep_json(langu=langu)
                if temp == "":
                    continue
                json_list.append(temp)
                new_str = new_str +temp
                new_str = new_str +'<br/>'
                print temp
                print "\n"
            print '\n\n'
            new_str = new_str+'<br/>'
        return new_str

    @staticmethod
    def get_category_csv(category,languages_list):
        new_str = ""
        json_list = []
        for stick in Sticker.objects.filter(category=category):

            new_str = new_str+'<br/>'
        return new_str

class Sticker(models.Model):
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=20)
    like = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date added',auto_now_add=True, blank=True)
    time = models.IntegerField(default=-1)

    def __str__(self):
        return ''.join([self.category,'-',self.name[4:]]).strip(".png")

    def is_hot(self,threshold_rating):
        if self.rating >= threshold_rating:
            return True
    def get_like(self):
        return self.like

    def update_likes(self, increment):
        self.like += increment

    def was_recently_added(self, stale_threshold=7):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=stale_threshold)

    def get_tags(self):
        for tag in self.tag_set.all():
            return ""

    @staticmethod
    def get_category_stickers(category):
        return Sticker.objects.filter(category=category)



    def del_all_tags(self):
        k = self.tag_set.all()
        k.delete()
        self.time = -1
        return True

    def delete_response_tags(self):
        resp_tags = self.tag_set.filter(theme='response')
        for tg in resp_tags:
            tg.delete()
        return True


    def get_tag_set(self):
        for tg in self.get_tag_set():
            print tg.name


    def get_lang_dep_json(self,langu):
        spl = {"*ctheme":[],"*cemotion":[],"*cfeeling":[],"*cbehaviour":[],"*creaction":[],"*csmiley":[],"*cresponse":[],"*cgeneral":[],"*cother":[],"*ctitle":[]}
        spl['lang'] = langconv[langu]
        spl['catId'] = self.category
        spl['sIds'] = self.name
        spl["*atime"] = self.time
        spl["*afestival"] = []
        count = 0;
        for tg in  self.tag_set.filter(lang=langu):
	    try:
	        spl[tagthem_inv[str(tg.theme).strip(' ')]].append(tg.name)
                count = count + 1
	    except:
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print self.name
		print tg.name
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
		print "\n################\n" 
        str_json = json.dumps(spl)
        if (langu == 'english') or (count > 0):
            return str_json
        else:
            return ""

    def lang_get_tagnames_for_theme(self,lang_tags,tagtheme):
        return get_names_of_list(lang_tags.filter(theme=tagtheme))

    def get_tagnames_for_theme(self,tagtheme):
        return get_names_of_list(list_to = self.tag_set.filter(theme=tagtheme))


    def make_json(self):
        """
        :return:""

        """
        """ {
        "cat_id": [cat_id1]
        "sIds" : ["sticker_id.png"],
        "CTheme" : ["theme1", "theme2"],
        "CEmotion" : ["emotion1", "emotion2","emotion3", "r1:emotion", "r3:emotion"],
        "CFeeling" : ["feeling1", "feeling2" , "feeling3", "r4:feeling" ],
        "CBehaviour" : ["behaviour1", "behaviour2" , "behaviour3" , "r4:behaviour" ],
        "CReaction" : ["reaction1", "reaction2" , "reaction3","r4:reaction4"  ],
        "CSmiley" : ["smiley1", "smiley2", "smiley3" ],
        "CResponse" : ["response1", "response2", "response3" ],
        "CGeneral" : ["general1", "general2", "general3" , "r3:general4", "r3:general5" ],
        "COther" : ["other1", "other2", "other3" ],
        "CTitle" : ["ctitle1"]
        "*ATime" : ["atime1"]
        },"""
        josn = {}
        josn["catId"] = self.category
        josn["sIds"] = self.name
        josn["*atime"] = self.time
        josn["*afestival"] = []
        for k,v in tagthem.items():
            josn[k] = self.get_tagnames_for_theme(tagtheme=v)
            #josn.update({"*atime" : -1})
        return josn

    def make_json_str(self):
        return str(self.make_json()).replace("u'","'")

    def make_str_json(self):
        return json.dumps(self.make_json())


class Tag(models.Model):
    sticker = models.ForeignKey(Sticker)
    name = models.CharField(max_length=100 )
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    #theme =["THEME","EMOTION","FEELING","BEHAVIOUR","REACTION","SMILEY","RESPONSE","GENERAL","OTHER","REGIONAL"]
    theme = models.CharField(max_length=20)
    lang = models.CharField(max_length=20,default='english')
    def __str__(self):
        return self.name
    def change_lang(self,langua):
        self.lang = langua
        self.save()

class TagTheme(models.Model):
    name = models.CharField(max_length=20)
    tag = models.ForeignKey(Tag)
    def __str__(self):
        return self.name

class TagType(models.Model):
    name= models.CharField(max_length=20)

    def __str__(self):
        return self.name
#
# class Tag(models.Model):
#     #sticker = models.ForeignKey(Sticker)
#     name = models.CharField(max_length=20)
#     upvotes = models.IntegerField(default=0)
#     downvotes = models.IntegerField(default=0)
#     theme = models.ForeignKey(TagType)
#
#     def __str__(self):
#         return self.name
#     #theme =["THEME","EMOTION","FEELING","BEHAVIOUR","REACTION","SMILEY","RESPONSE","GENERAL","OTHER","REGIONAL"]
#
#
# class TagTheme(models.Model):
#     name = models.CharField(max_length=20)
#     sticker = models.ForeignKey(Sticker)
#     def __str__(self):
#         return self.name




    @staticmethod
    def get_all_types():
        return TagType.objects.all()


class LangType(models.Model):
    name= models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_languages():
        return LangType.objects.all()
