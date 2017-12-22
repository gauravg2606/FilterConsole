from django import forms
from .enums import FILTER_TYPES
from .enums import FACE_FILTER_EFFECT_TYPES
from .enums import OPERATION_TYPES
from .enums import AVAILABILITY_STATUS



class FilterForm(forms.Form):

    DATE_FORMAT = '%m/%d/%Y'
    TIME_FORMAT = '%I:%M %p'
    fileToUpload = forms.FileField(label="Asset File")
    assetId = forms.CharField(label='Asset ID', max_length=100,widget = forms.HiddenInput(),required=False)
    # name = forms.CharField(label="Name",max_length=100)
    type = forms.ChoiceField(choices=FILTER_TYPES,label=" Filter Type")
    androidAppVersion = forms.CharField(label="Android App Version",max_length=20,required=False)
    androidOsVersion = forms.CharField(label='Android OS Version',max_length=20,required=False)
    iosAppVersion = forms.CharField(label="iOS App Version",max_length=20,required=False)
    iosVersion = forms.CharField(label='iOS Version',max_length=20,required=False)
    op = forms.ChoiceField(choices=OPERATION_TYPES,label="Operation Type",widget = forms.HiddenInput(),required=False)
    effectType = forms.ChoiceField(choices=FACE_FILTER_EFFECT_TYPES, label = "effectType", required=False)
    # gg : category for asset
    category = forms.CharField(label="Category", max_length=20, required=True, initial = "None")
    status = forms.ChoiceField(choices=AVAILABILITY_STATUS,label="Availability Status",widget = forms.HiddenInput(),required=False)
    expiryDate = forms.DateField(label="Expiry Date",widget=forms.SelectDateWidget())
    expiryTime = forms.TimeField(label="Expiry Time",widget=forms.widgets.TextInput(attrs={'placeholder': 'hh:mm'}))

class CategoryImageForm(forms.Form):
    fileToUpload = forms.FileField(label="Category Image File", required=True)
    categoryId = forms.CharField(label='CategoryId', max_length=100,widget = forms.HiddenInput(),required=False)
    filterType = forms.ChoiceField(choices=FILTER_TYPES,label=" Filter Type", required=True)
    category = forms.CharField(label="Category", max_length=20, required=True)

class AssetForm(forms.Form):
    fileToUpload = forms.FileField(label="Asset File")

#gg : AssetOrderForm
class FetchAssetOrderForm(forms.Form):
    filterType = forms.ChoiceField(choices = FILTER_TYPES, label=" Filter Type")
    categoryType = forms.CharField(label=" Category")
    # #categoryType = forms.ChoiceField(label=" Category")
    #categoryType = forms.ChoiceField(label = "Category", required=True, widget=forms.Select(attrs={'required':'required'}))
    # filterType = forms.ModelChoiceField(queryset=FilterType.objects.values_list('type', flat = True))
    # categoryType = forms.ModelChoiceField(queryset=Category.objects.none())


#gg : CategoryOrderForm
class FetchCategoryOrderForm(forms.Form): 
    type = forms.ChoiceField(choices=FILTER_TYPES, label=" Filter Type")

class DeleteAssetForm(forms.Form):
    assetName = forms.CharField(label="Asset Name", max_length=20, required=True, initial=None);

class FetchAssetForm(forms.Form):
    type = forms.ChoiceField(choices=FILTER_TYPES, label=" Filter Type")