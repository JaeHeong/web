from django.forms import ModelForm

from .models import *

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']

class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = ['title', 'imgfile', 'content']