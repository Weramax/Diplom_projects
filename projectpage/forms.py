from django import forms
from .models import Comment

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=50)
    file = forms.FileField()

class CommentForm(forms.Form):
    text = forms.CharField(max_length=50)
