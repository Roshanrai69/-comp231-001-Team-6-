from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'description','image')
        widgets = {
            'url': forms.HiddenInput,
            'image': forms.FileInput(attrs={'onchange': 'previewImage(event)'})
        }




