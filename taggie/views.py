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

["THEME","EMOTION","FEELING","BEHAVIOUR","REACTION","SMILEY","RESPONSE","GENERAL","OTHER","REGIONAL"]

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
    print "sticker id is "+str(sticker_id)
    try:
        sticker = get_object_or_404(Sticker,pk=sticker_id)
    except:
        return render(request,'taggie/404.html',{})
    return render(request,'taggie/detail.html',{'sticker':sticker,'tag_types':tag_types,'sticker_json':sticker.make_json_str()})

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
        return False
    except Exception as e:
        print "2"+e.message
        return False
    return True

@login_required(login_url='/login/')
def add(request,sticker_id):
    #print request
    s = get_object_or_404(Sticker,pk=sticker_id)


    try:
        theme_type = request.POST['tag_type']
        hash_tags = str(request.POST.get('tag'))
    except:
        return HttpResponseRedirect('/tag/'+sticker_id,{'sticker_json':s.make_json_str()})

    tag_set = hash_tags.strip(" ").replace('#',"").split(',')
    tag_themes_list =  request.POST.get('tag_type',[])
    print "tag_type "+str(tag_themes_list)
    for htag in tag_set:
        if htag == "":
            continue
        try:
            ta = s.tag_set.get(name=htag)
            ta.upvotes += 1
            ta.save()
            #add_tagtypes(ta.id, tag_themes_list)
        except ObjectDoesNotExist:
            ta = s.tag_set.create(name=htag,theme=str(theme_type))
            s.save()
        if tag_themes_list is not None:
            if add_tagtypes(ta.id, tag_themes_list):
                print "Tag themes added"
            else:
                print "Tag themes not updated"
    # return HttpResponseRedirect("/tag/"))
    return HttpResponseRedirect('/tag/'+sticker_id)
# def add(request, ,sticker_id, tag):
#     sticker = get_object_or_404(Sticker,pk=sticker_id)
#     try:
#         added_tag = sticker.tag_set.get()
#     return ""

@login_required(login_url='/login/')
def category(request,catid):
    # lister = category_stickers_list
    print "catid is"+str(catid)
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
            return  render(request,'taggie/search.html',{'error_message':"Atleast three  characters to search for"}) #error_message

    except:
        return  render(request,'taggie/search.html',{'error_message':"Please fill the search field"}) #error_message
    res = search_for(term=srch_word)
    print "reuslt s "+str(res)
    if not res:

        return  render(request,'taggie/search.html',{'error_message':"No results found"}) #error_message
    return render(request,'taggie/search.html',{'results':res})

@login_required
def search_stickers(request,sticker_nm):
    print request
    # print "\nsticker serach temr"+str(sticker_nm)
    if sticker_nm is None:
        return HttpResponseRedirect('/tag/')
    res = search_for(term=sticker_nm)
    print str(res)
    return render(request,'taggie/search.html',{'results':res})




@login_required(login_url='/login/')
def logger_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@basic_http_auth
def auth_tester(request):
    return HttpResponse("You are authenticated")