from django import forms

class Locationform(forms.Form):
    Enter_your_location = forms.CharField(max_length=100)