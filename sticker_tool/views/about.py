__author__ = 'hitesh'
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class IndexPageView(TemplateView):
    template_name = "index.html"