# forms.py
from django import forms

class WordUploadForm(forms.Form):
    file = forms.FileField(label="Upload Word File")
    state = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter State (e.g. Arunachal Pradesh)"
        })
    )
