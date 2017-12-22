from __future__ import unicode_literals

from django.db import models

# Create your models here.
# class FilterType(models.Model):
#     type = models.CharField(choices = FILTER_TYPES,)
#     filter_name = models.CharField(max_length = 20)
#     stream = models.CharField(max_length = 15)
#     number_of_sem = models.IntegerField(max_length = 2)
#     category_id = models.CharField(primary_key)


#     def __unicode__(self):
#         return self.course_id

# class batch(models.Model):
#     batch_id = models.CharField(primary_key = True, max_length = 20)
#     course_id = models.ForeignKey(course)
#     session = models.IntegerField("Year of the batch", max_length = 10)

#     def __unicode__(self):
#         return self.batch_id

# 		

# class FilterType(models.Model):
# 	type = models.CharField(choices=FILTER_TYPES, blank = False, primary_key = True);

# 	def __unicode__(self):
#          return self.type;

# class Category(models.Model):
# 	category = models.ForeignKey(FilterType);

# 	def __unicode__(self):
#          return self.category;