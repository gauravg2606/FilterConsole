##Gen imports
import datetime
## Django imports
from django.db import models
from django.utils import timezone

# Create your models here.

tagthem = {"CTheme":"theme","CEmotion":"emotion","CFeeling":"feeling","CBehaviour":"behaviour","CReaction":"reaction","CSmiley":"smiley","CResponse":"response","CGeneral":"general","COther":"other","AFestival":"festival"}


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



class Sticker(models.Model):
    name = models.CharField(max_length=40)
    category = models.CharField(max_length=20)
    like = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date added',auto_now_add=True, blank=True)

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




    def get_tagnames_for_theme(self,tagtheme):
        return get_names_of_list(list_to = self.tag_set.filter(theme=tagtheme))

    def make_json(self):
        """
        :return:""

        """
        """ {
        "cat_id": [cat_id1]
        "sticker" : ["sticker_id.png"],
        "CTheme" : ["theme1", "theme2"],
        "CEmotion" : ["emotion1", "emotion2","emotion3", "r1:emotion", "r3:emotion"],
        "CFeeling" : ["feeling1", "feeling2" , "feeling3", "r4:feeling" ],
        "CBehaviour" : ["behaviour1", "behaviour2" , "behaviour3" , "r4:behaviour" ],
        "CReaction" : ["reaction1", "reaction2" , "reaction3","r4:reaction4"  ],
        "CSmiley" : ["smiley1", "smiley2", "smiley3" ],
        "CResponse" : ["response1", "response2", "response3" ],
        "CGeneral" : ["general1", "general2", "general3" , "r3:general4", "r3:general5" ],
        "COther" : ["other1", "other2", "other3" ],
        "AFestival" : ["festival1"]
        },"""
        josn = {}
        josn["cat_id"] = [self.category]
        josn["sticker"] = [self.name]
        for k,v in tagthem.items():
            josn[k] = self.get_tagnames_for_theme(tagtheme=v)

        return josn

    def make_json_str(self):
        return str(self.make_json()).replace("u'","'")



class Tag(models.Model):
    sticker = models.ForeignKey(Sticker)
    name = models.CharField(max_length=30)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    #theme =["THEME","EMOTION","FEELING","BEHAVIOUR","REACTION","SMILEY","RESPONSE","GENERAL","OTHER","REGIONAL"]
    theme = models.CharField(max_length=20)
    def __str__(self):
        return self.name


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

