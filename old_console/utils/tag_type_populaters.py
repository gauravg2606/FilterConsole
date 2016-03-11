__author__ = 'patley'
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StickerTagger.settings")

    from django.core.management import execute_from_command_line

    import django
    django.setup()
    from taggie.models import Sticker, TagType

    f = open("tag_types.txt","r")
    print "read file"
    for line in f:
        data = line.strip("\r\n").strip(" ")
        if data !="":
            try:
                print data
                s = TagType(name=data)
                s.save()
            except:
                print "except"+str(data)
                print str(len(data))
    print "Done"