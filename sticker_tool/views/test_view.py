__author__ = 'hitesh'
from django.shortcuts import render
from django.views.generic import TemplateView
from sticker_tool.db import get_dropboxstickerdb_instance
# Create your views here.
class DropboxPageView(TemplateView):
    template_name = "test_view.html"
