from django import forms

class Registration(forms.Form):
    given_name = forms.CharField()