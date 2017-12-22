__author__ = 'hitesh'

from django.shortcuts import render
from django.views.generic import TemplateView
from sticker_tool.db import get_dropboxstickerdb_instance
# Create your views here.
class DropboxPageView(TemplateView):
    template_name = "dropboxdata.html"

    def get_context_data(self, **kwargs):
        context = super(DropboxPageView, self).get_context_data(**kwargs)
        sticker_pack_details = list()
        cat_icons_exist = False
        flag = False
        mongdb = get_dropboxstickerdb_instance()
        try:
            query = mongdb.dropboxdata_200.find()
            for data in query:
                catId = data['catId']
                sticker_preview = data['stickers_info'][0]['sticker_link']
                cat_icons = data['category_icon']
                if len(cat_icons) > 0:
                    cat_icons_exist = True
                sticker_pack_details.append((catId, sticker_preview, cat_icons_exist))
                print(sticker_pack_details)
        except Exception as e:
            print(e.message)
        context['sticker_pack_details'] = sticker_pack_details
        return context


