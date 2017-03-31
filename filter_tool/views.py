from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import FilterForm
from .forms import AssetForm
from django.http import JsonResponse
from django.http import HttpResponse
import time
import json
import requests
# Create your views here.
class FilterUpload(TemplateView):
    def get(self, request, *args, **kwargs):
        filter_upload_form = FilterForm();
        asset_upload_form = AssetForm();
        template_name = "form.html"
        return render(request, template_name, {'filter_form': filter_upload_form,'asset_form':asset_upload_form})

def launchView(request):
    template_name = 'filter_launch.html'
    return render(request,template_name)

def launch(request):
    urlLaunch = 'http://staging.im.hike.in/v2/ota_console/launch';
    responseLaunch = requests.post(urlLaunch)
    if(responseLaunch.status_code >= 200 and responseLaunch.status_code < 400):
        responseText = responseLaunch.json().get("stat");
        if(responseText == 'ok'):
            return HttpResponse("Successfully Launched")
        else:
            return HttpResponse("There was some error in launching")


def upload_asset(request):
    if(request.method == 'POST'):
        currentForm = FilterForm(request.POST, request.FILES);
        urlAsset = 'http://dev-bots.hike.in/ams/v1/assets'
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
            r = requests.post(urlAsset, files=files,data={"type":'jpeg'})
            if(r.status_code >= 200 and r.status_code < 400):
                assetId = r.json().get("assetId");
                print assetId;
                filterResponseAndroid = False;
                filterResponseIOS = False;
                if (android == True):
                    filterResponseAndroid =  upload_filter(assetId,"android",currentForm);
                if(ios == True):
                    filterResponseIOS = upload_filter(assetId,"ios",currentForm);
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
                return HttpResponse("Errors uploading Asset. Try again");

        else:
            print currentForm.errors
            return HttpResponse(currentForm.errors);

def upload_filter(assetId,devType,currentForm):
    urlFilter = "http://staging.im.hike.in/v2/ota_console/asset"
    hour =  currentForm.cleaned_data["expiryTime"].hour
    min = currentForm.cleaned_data["expiryTime"].minute
    dataFilter={
        "assetId" : assetId,
        "name":currentForm.cleaned_data["name"],
        "type" : currentForm.cleaned_data["type"],
        "devType":devType,
        "op":1,
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
        return int(time.mktime(value.timetuple())*1000 + (hour*60*60 - 5.5*60*60 +min*60)*1000)
    except AttributeError:
        return ''

