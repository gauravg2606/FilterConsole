##Gen imports
import datetime
## Django imports
from django.db import models
from django.utils import timezone

# Create your models here.

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
        for tag in Sticker.tag_set.all():
            return ""
    @staticmethod
    def get_category_stickers(category):
        return Sticker.objects.filter(category=category)


class Tag(models.Model):
    sticker = models.ForeignKey(Sticker)
    name = models.CharField(max_length=20)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    #theme =["THEME","EMOTION","FEELING","BEHAVIOUR","REACTION","SMILEY","RESPONSE","GENERAL","OTHER","REGIONAL"]

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

    @staticmethod
    def get_all_types():
        return TagType.objects.all()

