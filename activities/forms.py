## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file defines the objects that uploaded files will be assigned to

## file modified from example at:
## https://github.com/Chive/django-multiupload/blob/master/examples/simple/forms.py

from django import forms
from multiupload.fields import MultiFileField

class UploadActivitiesForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)