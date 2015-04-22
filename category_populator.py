__author__ = 'patley'
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StickerTagger.settings")

    from django.core.management import execute_from_command_line

    import django
    django.setup()
    from taggie.models import Sticker,Category

    f = open("stickers_cat.txt","r")

    for line in f:
        data = line.strip("\r\n").strip(" ").split(",")
        if data !="":
            try:
                c = Category(name=data[0],banner=data[1])
                c.save()
            except Exception as e:
                print str(e)
                print data
                print str(len(data))
    print "Done"