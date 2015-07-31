from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from taggie.models import *
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.
from functools import wraps
import base64
import logging

logger = logging.getLogger('taggie')

["THEME","EMOTION","FEELING","BEHAVIOUR","REACTION","SMILEY","RESPONSE","GENERAL","OTHER","REGIONAL"]

LANGUAGES_LIST  = LangType.get_all_languages()
tag_types = TagType.get_all_types()

@login_required(login_url='/login/')
def index(request):
    # return HttpResponse("Hello, from django world")
    latest_stickers_list = Sticker.objects.order_by('-pub_date')[:25]
    context = {'latest_stickers_list':latest_stickers_list}
    return render(request,'taggie/index.html',context)

@login_required(login_url='/login/')
def details(request, sticker_id):
    #print request
    #print "sticker id is "+str(sticker_id)
    logger.info("Sticker id is "+sticker_id)
    try:
        sticker = get_object_or_404(Sticker,pk=sticker_id)
    except:
        return render(request,'taggie/404.html',{})
    user_id = request.user
    return render(request,'taggie/detail.html',{'sticker':sticker,'tag_types':tag_types,'sticker_json':sticker.make_json_str(),'user':str(user_id),"lang_options":LANGUAGES_LIST})

@login_required(login_url='/login/')
def results(request,sticker_id):
    response = "You are looking at the results of the Sticker %s"
    return HttpResponse(response % sticker_id)

@login_required(login_url='/login/')
def vote(request, sticker_id):
    return HttpResponse("You are voting on sticker %s " % sticker_id)

#@login_required(login_url='/login/')
def add_tagtypes(tag_id,tags_types):
    """ Adds tag types to the tag with given id
    :param tags_types: List containing name of tagtypes
    :return:
    """
    try:
        tag_ = Tag.objects.get(pk=tag_id)
        for tag_type in tag_types:
            try:
                tag_.tagtheme_set.get(name=tag_type)
            except ObjectDoesNotExist:
                tag_.tagtheme_set.create(name=tag_type)
    except ObjectDoesNotExist as e:
        print "1"+e.message
        logger.debug("1"+e.message)
        return False
    except Exception as e:
        print "2"+e.message
        logger.debug("2"+e.message)
        return False
    return True

@login_required(login_url='/login/')
def add(request,sticker_id):
    #print request
    s = get_object_or_404(Sticker,pk=sticker_id)
    tagtypes_list = tagthem.values()

    print "request.POST "+ str(request.POST)
    for tagtype in tagtypes_list:
        taglist = []
        try:
            taglist = request.POST.getlist(tagtype)
        except:
            return HttpResponseRedirect('/tag/'+sticker_id,{'sticker_json':s.make_json_str()})
        taglist = [x.encode('UTF8') for x in taglist]
        taglist = taglist[0].split(',')
        taglist = [x.strip() for x in taglist]
        if len(taglist[0]) == 0:
            taglist = []
        for tag in taglist:
            print "tag " + str(tag) + " of type " + str(tagtype)
            if tag == "":
                continue
            if str(tagtype) == 'time':
                print "setting atime"
                s.time=int(tag)
                s.save()
                continue
            try:
                ta = s.tag_set.get(name=tag)
                ta.save()
                print str(tag) + " already exists!"
            #add_tagtypes(ta.id, tag_themes_list)
            except ObjectDoesNotExist:
                ta = s.tag_set.create(name=tag,theme=tagtype)
                s.save()
                print "Adding " + str(tag) + " to " + str(tagtype)
            if add_tagtypes(ta.id, [str(tagtype)]):
                print "Tag types added"
                logger.info("Tag types added")
            else:
                print "Tag types not updated"
                logger.debug("Tag types not updated")

    return HttpResponseRedirect('/tag/'+sticker_id)

@login_required(login_url='/login/')
def category(request,catid):
    # lister = category_stickers_list
    #print "catid is"+str(catid)
    context ={"category_stickers_list":Sticker.get_category_stickers(catid),"category":catid}
    return render(request,'taggie/category.html',context)

@login_required(login_url='/login/')
def cat_list(request):
    categ_list = Category.get_all_categories()
    return render(request,'taggie/cat_index.html',{'categories_list':categ_list} )


def basic_http_auth(f):
    def wrap(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION', False):
            authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
            auth = base64.b64decode(auth)
            username, password = auth.split(':')
            if username == 'foo' and password == 'bar':
                return f(request, *args, **kwargs)
            else:
                r = HttpResponse("Auth Required", status = 401)
                r['WWW-Authenticate'] = 'Basic realm="bat"'
                return r
        r = HttpResponse("Auth Required", status = 401)
        r['WWW-Authenticate'] = 'Basic realm="bat"'
        return r

    return wrap

@login_required
def search_stick(request):
    try:
        if request.GET['search'] != "":
            srch_word = request.GET['search']
        else:
            return  render(request,'taggie/search.html',{'error_message':"Please fill the search field"}) #error_message
        if len(request.GET['search']) >= 3:
            srch_word = request.GET['search']
        else:
            return  render(request,'taggie/search.html',{'keyterm':srch_word,'error_message':"Atleast three  characters to search for"}) #error_message

    except:
        return  render(request,'taggie/search.html',{'error_message':"Please fill the search field"}) #error_message
    res = search_for(term=srch_word)
    print "reuslt s "+str(res)
    if not res:

        return  render(request,'taggie/search.html',{'keyterm':srch_word,'error_message':"No results found"}) #error_message
    return render(request,'taggie/search.html',{'keyterm':srch_word,'results':res})

@login_required
def search_stickers(request,sticker_nm):
    #print request
    # print "\nsticker serach temr"+str(sticker_nm)
    if sticker_nm is None:
        return HttpResponseRedirect('/tag/')
    res = search_for(term=sticker_nm)
    print str(res)
    return render(request,'taggie/search.html',{'results':res})


@login_required
def delete_tags(request):

    try:
        sticker_id = request.POST['sid']
        sticker = get_object_or_404(Sticker,pk=sticker_id)
    except:
        return render(request,'taggie/404.html',{})
    tags_l = sticker.del_all_tags()
    return HttpResponseRedirect('/tag/'+sticker_id,{'sticker_json':sticker.make_json_str()})


@login_required
def delete_response_tags(request):

    try:
        sticker_id = request.POST['sid']
        sticker = get_object_or_404(Sticker,pk=sticker_id)
    except:
        return render(request,'taggie/404.html',{})
    tags_l = sticker.delete_response_tags()
    return HttpResponseRedirect('/tag/'+sticker_id,{'sticker_json':sticker.make_json_str()})


@login_required(login_url='/login/')
def logger_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@basic_http_auth
def auth_tester(request):
    return HttpResponse("You are authenticated")

@login_required(login_url='/login/')
def gisc_finale(request):
    print str(request.user)
    return render(request,'taggie/finale.html')

def get_categ_json(request,categ='humanoid'):
    print "get_categ_json " + categ
    som = Category.get_category_json_lang(categ,langconv.keys())
    return HttpResponse(som)

@login_required(login_url='/login/')
def language_updater(request):
    if (not request.POST.get('language')) or (not request.POST.get('tag_set')) or (not request.POST.get("sid")):
        return HttpResponse("You have not filled the required fields")

    try:
        sticker_id =  request.POST.get("sid")
        sticker = get_object_or_404(Sticker,pk=sticker_id)
    except:
        return render(request,'taggie/404.html',{})

    for tg in  request.POST.getlist('tag_set'):
        try:
            ptag = Tag.objects.get(pk=tg)
            ptag.change_lang(request.POST.get('language').strip().lower())
        except Exception as e:
            print "Exeption is "+e.message
    return HttpResponseRedirect('/tag/'+sticker_id,{'sticker_json':sticker.make_json_str()})
