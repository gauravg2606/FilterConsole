__author__ = 'patley'
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StickerTagger.settings")

    from django.core.management import execute_from_command_line

    import django
    django.setup()
    from taggie.models import Sticker
    BASE_URL  = "/Users/patley/hello/stickers/"
    f = open(BASE_URL+"lovequotes_pack_stk_packs_list.csv","r")

    for line in f:
        print "data "+str(line)
        data = line.strip("\r\n").strip(" ").split(",")
        if data !="":
            try:
                s = Sticker(name=data[1],category=data[0])

                s.save()
                print "added sticker"
            except:
                print data
                print str(len(data))
    print "Done"