from django import forms
from .enums import FILTER_TYPES
from .enums import PLATFORM_TYPES
from .enums import OPERATION_TYPES
from .enums import AVAILABILITY_STATUS
class FilterForm(forms.Form):
    fileToUpload = forms.FileField(label="Asset File")
    assetId = forms.CharField(label='Asset ID', max_length=100,widget = forms.HiddenInput(),required=False)
    name = forms.CharField(label="Name",max_length=100)
    type = forms.ChoiceField(choices=FILTER_TYPES,label=" Filter Type")
    androidAppVersion = forms.CharField(label="Android App Version",max_length=20,required=False)
    androidOsVersion = forms.CharField(label='Android OS Version',max_length=20,required=False)
    iosAppVersion = forms.CharField(label="iOS App Version",max_length=20,required=False)
    iosVersion = forms.CharField(label='iOS Version',max_length=20,required=False)
    op = forms.ChoiceField(choices=OPERATION_TYPES,label="Operation Type")
    status = forms.ChoiceField(choices=AVAILABILITY_STATUS,label="Availability Status")
    expiry = forms.DateTimeField(label="Expiry Time",widget=forms.SelectDateWidget())

class AssetForm(forms.Form):
    fileToUpload = forms.FileField(label="Asset File")