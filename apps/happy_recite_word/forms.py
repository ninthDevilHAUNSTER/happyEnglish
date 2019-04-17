from django import forms


class WordUpdateFrom(forms.Form):
    en_word = forms.CharField(max_length=200, label="英语单词")
    cn_word = forms.CharField(max_length=200, label="中文解释")


from django.forms import ModelForm
from .models import ExcelStatus


class UploadFileForm(ModelForm):
    class Meta:
        model = ExcelStatus
        fields = ('xl_file',)
