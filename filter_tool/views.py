from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import FilterForm
from .forms import FetchOrderForm
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
        template_name = "form.html"
        return render(request, template_name, {'filter_form': filter_upload_form,"title":settings.HEADER_TITLE})


def launch(request):
    urlLaunch = settings.LAUNCH_FILTERS_URL;
    responseLaunch = requests.post(urlLaunch)
    if(responseLaunch.status_code >= 200 and responseLaunch.status_code < 400):
        responseText = responseLaunch.json().get("stat");
        if(responseText == 'ok'):
            return HttpResponse("Successfully Launched")
        else:
            return HttpResponse("There was some error in launching")


def orderUpdate(request):
    jsonData = json.loads(request.body);
    if request.method == 'POST':
        urlUpdateOrder = settings.UPDATE_FILTERS_ORDER_URL
        responseUpdate = requests.post(urlUpdateOrder,json=jsonData);
        if(responseUpdate.status_code >=200 and responseUpdate.status_code < 400):
            return JsonResponse({"success":"Received"})
        else:
            return JsonResponse({"error":"There was some error updating order"});

def orderForm(request):
    type = request.GET.get('type');
    template_name = "form_order.html";
    if(type is not None):
        data={'type':type}
        fetchOrderForm = FetchOrderForm(initial=data);
        urlFetch = settings.FETCH_FILTERS_ORDER_URL+type;
        r = requests.get(urlFetch);
        if(r.status_code >= 200 and r.status_code < 400):
            data = r.json();
            return render(request,template_name,{'fetch_form':fetchOrderForm,'type':type,'data':data,"title":settings.HEADER_TITLE})
        else:
            return render(request,template_name,{'fetch_form':fetchOrderForm,'type':type,'error':"There was some error getting current order","title":settings.HEADER_TITLE})
    else:
        fetchOrderForm = FetchOrderForm();
        return render(request,template_name,{'fetch_form':fetchOrderForm,"title":settings.HEADER_TITLE})


def upload_asset(request):
    if(request.method == 'POST'):
        currentForm = FilterForm(request.POST, request.FILES);
        urlAsset = settings.UPLOAD_ASSET_URL
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
    urlFilter = settings.UPLOAD_FILTER_URL
    hour =  currentForm.cleaned_data["expiryTime"].hour
    min = currentForm.cleaned_data["expiryTime"].minute
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

