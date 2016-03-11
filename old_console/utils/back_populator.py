__author__ = 'candhare-hike'
#!/usr/bin/env python

# Script to back-populate SQL db of Taggie console from previously generated JSONs.
# It assumes that the JSONs given as input are free from any errors.
# Database in its current state before running this script should already be sanitized.
# There should not be any existing errors in mapping or the script may fail. For
# example, duplicate objects will cause get() methods to trigger an exception.
# This script must be in the root folder (StickerTaggingConsole/) of the Django site
# which contains the site config folder (StickerTaggingConsole/StickerTagger/) and
# the application folder (StickerTaggingConsole/taggie/), etc.
#
# Usage: python back_populator.py <file_containing_json_strings>
#
# This script will read json strings (assumed to be one (sticker, lang) on each line)
# and process each json as follows:
# 1. Create category in taggie_category if it doesn't exist.
# 2. Create sticker in taggie_sticker if it doesn't exist.
# 3. Set atime for the sticker.
# 4. For each tagtype:
# 4.1   Get list of tags.
# 4.2   For each tag in the list:
# 4.2.1    Create tag in taggie_tag table if it doesn't exist.
# 4.2.2    Create tagtype-to-tag mapping in the taggie_typetotag table if it doesn't exist.

import os
import sys
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StickerTagger.settings")
from taggie.models import *
from django.core.exceptions import ObjectDoesNotExist

# Map language names (for db) to their code names (for json)
langconv = {"english":"eng","hindi":"hin","marathi":"mar","hinglish":"hin","assamese":"asm","awadhi":"awa","bengali":"ben","bhojpuri":"bho","bundeli":"bns","chattisgarhi":"hne","dogri":"doi","garhwali":"gbm","gujarati":"guj","haryanvi":"bgc","hyderabadi":"dcc","kangri":"xnr","kannada":"kan","kashmiri":"kas","khariboli":"59-AAF-qd","kortha":"east2315","konkani":"kok","malayalam":"mal","malvi":"mup","oriya":"ori","punjabi":"pan","rajasthani":"raj","tamil":"tam","telugu":"tel","tulu":"tcy","urdu":"urd","garo":"grt","khasi":"kha","mizo":"lus","manipuri":"mni","kok borok":"trp","sikkim":"sip","nepali":"nep","bodo":"brx","lepcha":"lep","sindhi":"snd","nagamese":"nag","kumaoni":"kfy","maithili":"mai"}
langconv_inv = {v: k for k, v in langconv.items()}

# Map tagtype code names (for json) to their names (for db)
tagtypes = {"*ctheme":"theme","*cemotion":"emotion","*cfeeling":"feeling","*cbehaviour":"behaviour","*creaction":"reaction","*csmiley":"smiley","*cresponse":"response","*cgeneral":"general","*cother":"other","*ctitle":"title"}
tagtypes_inv = {v: k for k, v in tagtypes.items()}

if __name__ == "__main__":
    django.setup()
    try:

        with open(sys.argv[1]) as f:
            for i, line in enumerate(f):

                if (line == "\n"): # Ignore empty lines
                    continue

                slJson = json.loads(line) # Retrieve json object
                print "Processing line " + str(i+1) + "..."

                # Check if category exists. Else, create it
                try:
                    c = Category.objects.get(name=slJson["catId"].encode('ascii'))
                except ObjectDoesNotExist:
                    sys.stdout.write("EXCEPTION: Category " + slJson["catId"].encode('ascii') + " not found for sticker " + slJson["sId"].encode('ascii') + ". Creating...")
                    # Create new category
                    c = Category.objects.create(name=slJson["catId"],banner="")
                    print "done."

                # Check if sticker exists. Else, create it
                try:
                    s = Sticker.objects.get(name=slJson["sId"].encode('ascii'),category=slJson["catId"].encode('ascii'))
                except ObjectDoesNotExist:
                    sys.stdout.write("EXCEPTION: Sticker " + slJson["sId"].encode('ascii') + " not found. Creating...")
                    # Create new sticker
                    s = Sticker.objects.create(name=slJson["sId"].encode('ascii'),category=slJson["catId"].encode('ascii'))
                    print "done."

                # Set atime (language-independent, but will be processed for every language anyway)
                # For a sticker, last language processed will overwrite all others' value of atime
                sys.stdout.write("Setting: *atime ")
                s.time = int(slJson["*atime"])
                s.save()

                # Convert language code of current json object to language name.
                currentLang = langconv_inv[slJson["lang"]]

                # Add every tag from every tagtype
                for k, v in tagtypes.items(): # k is codename (e.g. '*ctitle'), v is simple name (e.g. 'title')
                    sys.stdout.write(k + " ")
                    taglist = slJson[k] # List of tags in json for type k
                    for t in taglist:

                        # Add tag to taggie_tag table
                        try:
                            tag = s.tag_set.get(name=t) # Does this tag already exist?
                        except ObjectDoesNotExist:
                            if (v == "theme"):
                                tag = s.tag_set.create(name=t,tagtype=v,lang='english') # Create theme tag in english only
                            else:
                                tag = s.tag_set.create(name=t,tagtype=v,lang=currentLang) # Create this tag
                            s.save()

                        # Add tag info to taggie_typestotag table (Mapping from tagtype to tag)
                        try:
                            tag.typestotag_set.get(name=v) # Does this mapping already exist?
                        except ObjectDoesNotExist:
                            tag.typestotag_set.create(name=v) # Create this mapping
                            tag.save()
                print ("done.")

    except Exception as e:
        print "Exception " + str(e) + " " + str(slJson)

