from django.shortcuts import render
from django.views.generic import TemplateView
from .forms2 import FilterForm
from .forms2 import FetchAssetOrderForm
from .forms2 import FetchCategoryOrderForm
from .forms2 import DeleteAssetForm
from .forms2 import FetchAssetForm
from .forms2 import CategoryImageForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
import time
import json
import requests
# Create your views here.
class FilterUpload(TemplateView):
    def get(self, request, *args, **kwargs):
        filter_upload_form = FilterForm();
        template_name = "form2.html"
        return render(request, template_name, {'filter_form': filter_upload_form,"title":settings.HEADER_TITLE})

class CategoryUpload(TemplateView):
    def get(self, request, *args, **kwargs):
        category_form = CategoryImageForm();
        template_name = "categoryImageUpload.html"
        return render(request, template_name, {'category_form': category_form,"title":settings.HEADER_TITLE})

def launch(request):
    urlLaunch = settings.LAUNCH_FILTERS_URL_V3;
    responseLaunch = requests.post(urlLaunch)
    if(responseLaunch.status_code >= 200 and responseLaunch.status_code < 400):
        responseText = responseLaunch.json().get("stat");
        if(responseText == 'ok'):
            return HttpResponse("Successfully Launched")
        else:
            return HttpResponse("There was some error in launching")

#----gg : for category order update-----

def categoryOrderUpdate(request):
    print request
    jsonData = json.loads(request.body);
    if request.method == 'POST':
        urlUpdateOrder = settings.UPDATE_CATEGORY_ORDER_URL_V3
        responseUpdate = requests.post(urlUpdateOrder, json=jsonData);
        if(responseUpdate.status_code >=200 and responseUpdate.status_code < 400):
            return JsonResponse({"success":"Received"})
        else:
            return JsonResponse({"error":"There was some error updating order"});

#------------------------------------------

#----gg : for assets for type-----

def fetchAssetForm(request):
    type = request.GET.get('type');
    template_name = "deleteAsset.html";
    if(type is not None):
        data={'type':type}
        fetchAssetForm = FetchAssetForm(initial=data, prefix='fetchForm', auto_id=False);
        urlFetch = settings.FILTERS_BY_TYPE+type;
        print urlFetch
        r = requests.get(urlFetch);
        if(r.status_code >= 200 and r.status_code < 400):
            data = r.json();
            print data
            return render(request,template_name,{'asset_form':fetchAssetForm,'type':type,'data':data,"title":settings.HEADER_TITLE})
        else:
            return render(request,template_name,{'asset_form':fetchAssetForm,'type':type,'error':"There was some error getting current asset for type","title":settings.HEADER_TITLE})
    else:
        fetchAssetForm = FetchAssetForm();
        return render(request,template_name,{'asset_form':fetchAssetForm,"title":settings.HEADER_TITLE})

#------------------------------------------
#----gg : for asset order update for particular type and particular category

def assetOrderUpdate(request):
    jsonData = json.loads(request.body);
    if request.method == 'POST':
        urlUpdateOrder = settings.UPDATE_FILTERS_ORDER_URL_V3
        print urlUpdateOrder
        print jsonData
        responseUpdate = requests.post(urlUpdateOrder, json=jsonData);
        print responseUpdate
        if(responseUpdate.status_code >=200 and responseUpdate.status_code < 400):
            return JsonResponse({"success":"Received"})
        else:
            return JsonResponse({"error":"There was some error updating order"});
#-------------------------------------------

#----gg : fetching category order for particular type

def fetchCategoryOrderForm(request):
    type = request.GET.get('type');
    template_name = "form_categoryOrder.html";
    if(type is not None):
        data={'type':type}
        fetchOrderForm = FetchCategoryOrderForm(initial=data);
        urlFetch = settings.FETCH_CATEGORY_ORDER_URL_V3+ type;
        print urlFetch
        r = requests.get(urlFetch);
        if(r.status_code >= 200 and r.status_code < 400):
            data = r.json();
            return render(request,template_name,{'fetch_form':fetchOrderForm,'type':type,'data':data,"title":settings.HEADER_TITLE})
        else:
            return render(request,template_name,{'fetch_form':fetchOrderForm,'type':type,'error':"There was some error getting current order","title":settings.HEADER_TITLE})
    else:
        fetchOrderForm = FetchCategoryOrderForm();
        return render(request,template_name,{'fetch_form':fetchOrderForm,"title":settings.HEADER_TITLE})
#---------------------------------------------------- 


#----gg : fetching Asset order for particular type and particular Category

def fetchAssetOrderForm(request):
    print request
    filterType = request.GET.get('filterType');
    categoryType = request.GET.get('categoryType');
    template_name = "form_assetOrder.html";
    if(filterType is not None and categoryType != None):
        data = {'filterType' : filterType, 'categoryType' : categoryType};
        fetchOrderForm = FetchAssetOrderForm(initial=data);
        urlFetch = settings.FETCH_FILTERS_ORDER_URL_V3+filterType+"&category="+categoryType;
        print urlFetch
        r = requests.get(urlFetch);
        if(r.status_code >= 200 and r.status_code < 400):
            data = r.json();
            print data
            return render(request, template_name, {'fetch_form':fetchOrderForm, 'data' : data, 'filterType' : filterType, 'category' : categoryType, 'title':settings.HEADER_TITLE});
        else :
            return render(request, template_name, {'fetch_form':fetchOrderForm, 'filterType' : filterType, 'category' : categoryType,'error':"There was some error getting current order","title":settings.HEADER_TITLE});

    else :
        fetchOrderForm = FetchAssetOrderForm();
        return render(request,template_name,{'fetch_form':fetchOrderForm,"title":settings.HEADER_TITLE})


#----------------------------------------------------

#-------gg: fetch category for a type to get assetOrder----

def getCategoryForType(request):
    print request
    filterType = request.GET.get('filterType');
    print filterType
    if(filterType is not None):
        urlFetch = settings.FETCH_CATEGORY_ORDER_URL_V3+filterType;
        print urlFetch
        r = requests.get(urlFetch);
        print r;
        if(r.status_code >= 200 and r.status_code < 400):
            return JsonResponse({'data': r.json()});
            # data = r.json();
            # print data;
            # return HttpResponse(r.json());

#----------------------------------------------------------

#-------gg: upload category Image ----

def categoryImageUpload(request):
    if(request.method == 'POST'):
        
        currentForm = CategoryImageForm(request.POST, request.FILES)
        if currentForm.is_valid():
            filterType = currentForm.cleaned_data['filterType']
            urlAsset = settings.UPLOAD_ASSET_URL_V3
            fileToUpload = request.FILES['fileToUpload']
            files = {'file': fileToUpload}
           
            file_type = fileToUpload.content_type.split('/')[1]
            name = fileToUpload.name.split('.'+file_type)[0];
            category = currentForm.cleaned_data['category']
            r = requests.post(urlAsset, files=files,data={"type":file_type})
            if(r.status_code >= 200 and r.status_code < 400):
                categoryId = r.json().get("assetId")
                print categoryId
                filterResponse =  updateCategoryId(categoryId,filterType,category);
         
                if(filterResponse and filterResponse.status_code >= 200 and filterResponse.status_code < 400):
                    return JsonResponse({"success":"Received"})
                else:
                    return JsonResponse({"error":"There was some error updating order"});
            else:
                print r.text;
                return HttpResponse("Errors uploading Asset. Try again");
        else:
            print currentForm.errors
            return HttpResponse(currentForm.errors);
#----------------------------------------------------------

def updateCategoryId(categoryId, filterType, category):
    urlFilter = settings.UPDATE_FILTERS_ORDER_URL_V3
    print "KK" + urlFilter
    if(filterType is not None):
        if(category is not None):
            dataFilter = {
                "type" : filterType,
                "category":category,
                "category_id":categoryId,
            }
            print dataFilter
            filterResponse = requests.post(urlFilter,json=dataFilter)
            return filterResponse


#-------gg: delete asset by type----

def deleteAssetForm(request):
    print request;
    assetName = request.GET.get('assetName');
    print assetName;
    if(assetName is not None):
        urlFetch = settings.DELETE_FILTER_BY_NAME_V3+assetName;
        print urlFetch
        responseDelete = requests.delete(urlFetch);
        if(responseDelete.status_code >=200 and responseDelete.status_code < 400):
            return JsonResponse({"success":"Deleted"})
        else:
            return JsonResponse({"error":"There was some error deleting asset"});

    

#----------------------------------------------------------

def upload_asset(request):
    if(request.method == 'POST'):
        currentForm = FilterForm(request.POST, request.FILES);
        urlAsset = settings.UPLOAD_ASSET_URL_V3
        fileToUpload = request.FILES['fileToUpload']
        files = {'file': fileToUpload}
        android = False;
        ios = False;
        if currentForm.is_valid():
            uploadAny = False;
            if(currentForm.cleaned_data["androidAppVersion"] != '' and currentForm.cleaned_data["androidOsVersion"]!= ''):
                android = True;
                uploadAny = True;
            if(currentForm.cleaned_data["iosAppVersion"] != '' and currentForm.cleaned_data["iosVersion"]):
                ios = True;
                uploadAny = True;
            if(uploadAny == False):
                return HttpResponse("Either Android or iOS fields needs to be filled ");
            file_type = fileToUpload.content_type.split('/')[1]
            name = fileToUpload.name.split('.'+file_type)[0];
            r = requests.post(urlAsset, files=files,data={"type":file_type})
            if(r.status_code >= 200 and r.status_code < 400):
                assetId = r.json().get("assetId");
                filterResponseAndroid = False;
                filterResponseIOS = False; 
                if (android == True):
                    filterResponseAndroid =  upload_filter(assetId,"android",currentForm,name);
                if(ios == True):
                    filterResponseIOS = upload_filter(assetId,"iPhone",currentForm,name);
                successAndroid = False;
                successIOS = False;

                if(filterResponseAndroid and filterResponseAndroid.status_code >= 200 and filterResponseAndroid.status_code < 400):
                    successAndroid = True;
                if(filterResponseIOS and filterResponseIOS.status_code >= 200 and filterResponseIOS.status_code < 400):
                    successIOS = True;
                    responseString = '';
                if (successAndroid == True and successIOS == True):
                    responseString = "Filter Uploaded successfully for both android with ObjectId "+filterResponseAndroid.json().get("ObjectId")+" and ios with ObjectId "+filterResponseIOS.json().get("ObjectId");
                elif(successAndroid == True):
                    responseString = "Filter Uploaded successfully for android with ObjectId "+filterResponseAndroid.json().get("ObjectId");
                elif(successIOS):
                    responseString = "Filter Uploaded for ios with ObjectId "+filterResponseIOS.json().get("ObjectId");
                else:
                    responseString = " Filter is not uploaded. Retry again";
                return HttpResponse(responseString);
            else:
                print r.text;
                return HttpResponse("Errors uploading Asset. Try again");

        else:
            print currentForm.errors
            return HttpResponse(currentForm.errors);

def upload_filter(assetId,devType,currentForm,filename):
    urlFilter = settings.UPLOAD_FILTER_URL_V3
    hour =  currentForm.cleaned_data["expiryTime"].hour
    min = currentForm.cleaned_data["expiryTime"].minute
    category = currentForm.cleaned_data["category"]
    filterEffectType = currentForm.cleaned_data["effectType"]
    print "kk"+currentForm.cleaned_data["effectType"]
    print category
    if(category is not None and category != ""):
        if(filterEffectType is not None):
            dataFilter={
            "assetId" : assetId,
            "name":filename,
            "type" : currentForm.cleaned_data["type"],
            "category" : currentForm.cleaned_data["category"],
            "effectType" : currentForm.cleaned_data["effectType"],
            "devType":devType,
            "op":0,
            "status":1,
            "expiry":epoch(currentForm.cleaned_data["expiryDate"],hour,min),
        }
        else :
            dataFilter={
                "assetId" : assetId,
                "name":filename,
                "type" : currentForm.cleaned_data["type"],
                "category" : currentForm.cleaned_data["category"],
                "devType":devType,
                "op":0,
                "status":1,
                "expiry":epoch(currentForm.cleaned_data["expiryDate"],hour,min),
            }
    else :
        dataFilter={
            "assetId" : assetId,
            "name":filename,
            "type" : currentForm.cleaned_data["type"],
            "devType":devType,
            "op":0,
            "status":1,
            "expiry":epoch(currentForm.cleaned_data["expiryDate"],hour,min),
        }
    if(devType == "android"):
        dataFilter["appVersion"] = currentForm.cleaned_data["androidAppVersion"];
        dataFilter["osVersion"] = currentForm.cleaned_data["androidOsVersion"];
    else:
        dataFilter["appVersion"] = currentForm.cleaned_data["iosAppVersion"];
        dataFilter["osVersion"] = currentForm.cleaned_data["iosVersion"];
    filterResponse = requests.post(urlFilter,json=dataFilter)
    return filterResponse

def epoch(value,hour,min):
    try:
        return int(time.mktime(value.timetuple()) + (hour*60*60 - 5.5*60*60 +min*60))
    except AttributeError:
        return ''

