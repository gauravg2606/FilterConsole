from django.contrib import admin
from taggie.models import Sticker, Tag ,Category, TagTheme , TagType ,LangType
# Register your models here.



class TagThemeInline(admin.TabularInline):
    model = TagTheme
    extra = 2
    list_display = ['name']

class TagInline(admin.TabularInline):
    model = Tag
    list_display = ['name']
    extra = 3
    inlines = [TagThemeInline]

class StickerAdmin(admin.ModelAdmin):
    # fields = ['name','category']
    inlines = [TagInline]
    fieldsets = [
        (None, {'fields':['name','category']}),
        # ('Tags',{'inlines':['inlines']})
    ]

class LangAdmin(admin.TabularInline):
    model = LangType
    extra = 2
    list_display = ['name']

admin.site.register(Sticker ,StickerAdmin)
admin.site.register(Category)
admin.site.register(TagTheme)
admin.site.register(TagType)
admin.site.register(LangType)
