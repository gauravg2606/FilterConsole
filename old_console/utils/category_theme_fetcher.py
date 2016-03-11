__author__ = 'patley'
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StickerTagger.settings")

    from django.core.management import execute_from_command_line

    import django
    django.setup()
    from taggie.models import *

    catgeory_str = sys.argv[1]
    categories_list = catgeory_str.split(",")
    theme_tags = []
    for item in categories_list:
        item = item.strip(" ").lower()
        print "Category "+str(item)
        for stick in Sticker.objects.filter(category='humanoid'):
            theme_tags = theme_tags + stick.get_tagnames_for_theme(tagtheme='theme')
        print "\n\n\n"

    print "\n\n\n\n\n"

    print theme_tags
    # f = open("stickers_list.csv","r")
    #
    # for line in f:
    #     data = line.strip("\r\n").strip(" ").split(",")
    #     if data !="":
    #         try:
    #             s = Sticker(name=data[1],category=data[0])
    #             s.save()
    #         except:
    #             print data
    #             print str(len(data))
    # print "Done"