from django import forms
from tmp_latex.youdao_craw import gen_words


class WordUpdateFrom(forms.Form):
    en_word = forms.CharField(max_length=200, label="英语单词")
    cn_word = forms.CharField(max_length=200, label="中文解释")


from django.forms import ModelForm
from .models import ExcelStatus


class UploadFileForm(ModelForm):
    class Meta:
        model = ExcelStatus
        fields = ('xl_file',)


from datetime import datetime, timedelta


class EnshrinedWordFilterForm(forms.Form):
    start_time = forms.DateTimeField(required=True,
                                     initial=(datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S"),
                                     widget=forms.DateTimeInput(
                                         attrs={'class': 'form-control'},
                                         format="%Y-%m-%d %H:%M:%S"
                                     ), help_text="起始时间"
                                     )
    end_time = forms.DateTimeField(required=True,
                                   initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   widget=forms.DateTimeInput(
                                       attrs={'class': 'form-control'},
                                       format="%Y-%m-%d %H:%M:%S"
                                   ), help_text="终止时间")
    least_enshrined_time = forms.IntegerField(required=True, initial=1,
                                              error_messages={
                                                  "required": "请输入最低收藏次数"
                                              }, help_text="收藏次数")

    def clean(self):
        if self.cleaned_data["end_time"] < self.cleaned_data["start_time"]:
            raise forms.ValidationError("请确认时间正确性")
        self.cleaned_data["start_time"] + timedelta(minutes=3)  # 我感觉我数据库的时间好像和djang的时间不太同步，所以都加了3分钟
        self.cleaned_data["end_time"] + timedelta(minutes=3)  # 我感觉我数据库的时间好像和djang的时间不太同步，所以都加了3分钟
        # try:
        #     datetime.strptime(self.cleaned_data["start_time"], '%Y-%m-%d %H:%M:%S')
        #     datetime.strptime(self.cleaned_data["end_time"], '%Y-%m-%d %H:%M:%S')
        # except ValueError:
        #     raise forms.ValidationError("请输入正确的时间格式： YYYY-MM-DD HH:MM:SS")
        return self.cleaned_data


class WordWriterForm(forms.Form):
    text_input = forms.CharField(required=True,
                                 initial="请输入内容，以回车代表每个单词的分隔",
                                 widget=forms.Textarea(
                                     attrs={'class': 'form-control'},
                                 ),
                                 help_text="请输入内容，以回车代表每个单词的分隔", )
    #
    # text_output = forms.CharField(required=False,
    #                               initial=" ",
    #                               widget=forms.TextInput(
    #                                   attrs={'class': 'form-control', 'disabled': 'False'},
    #                               ))

    # def clean(self):
    #     self.cleaned_data['text_output'] = gen_words(words=
    #                                                  self.cleaned_data['text_input'].split('\n'))
    #     return self.cleaned_data
