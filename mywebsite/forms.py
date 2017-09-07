# -*- coding=utf-8 -*-
"""表单"""

from django import forms

class homeworkform(forms.Form):
    author = forms.CharField()
    title = forms.CharField(required=True)
    urllink = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)