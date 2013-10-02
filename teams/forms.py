from django import forms

class UploadFileForm(forms.Form):
    groups = forms.FileField(label='Select a file')