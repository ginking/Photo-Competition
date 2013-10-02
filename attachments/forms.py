from mpc.settings import CATEGORY

from django import forms

class UploadPhotoForm(forms.Form):

    photo_file = forms.FileField(label='Select a file')

    photo_category = forms.ChoiceField(choices=CATEGORY)


#     def save(self, *args, **kwargs):
#         return super(UploadPhotoForm, self).save()

