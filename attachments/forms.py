from mpc.settings import CATEGORY

from django import forms

class UploadPhotoForm(forms.Form):

    photo_file = forms.FileField(label='Select a file')

    photo_category = forms.ChoiceField(choices=CATEGORY)

