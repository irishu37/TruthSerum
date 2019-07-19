from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.Form):
    class Meta:
        model = ImageUpload
        fields = ('file', )
