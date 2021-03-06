from django.db import models
from datetime import datetime
import django.utils.timezone as timezone
from django.core import validators
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from happyEnglish.settings import MEDIA_ROOT
from users.models import UserProfile
import os


# Create your models here.
class ExcelStatus(models.Model):
    name = models.CharField(max_length=50, default="", verbose_name="EXCEL 名称")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="创建日期")
    xl_file = models.FileField(upload_to="%Y/%m/%d/", validators=[
        validators.FileExtensionValidator(['xlsx', 'csv'])
    ], verbose_name="EXCEL 文件")
    recite_time = models.DateTimeField(default=datetime(2000, 1, 1, 1, 1, 1, 1), verbose_name="背诵日期")
    pdf_file = models.FileField(upload_to="pdfs/", validators=[
        validators.FileExtensionValidator(['pdf'])
    ], null=False, default="None", help_text="单词本")
    ans_file = models.FileField(upload_to="pdfs/", validators=[
        validators.FileExtensionValidator(['pdf'])
    ], null=False, default="None", help_text="答案本")
    owner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="owner", verbose_name="所有者")

    def __str__(self):
        return self.name


# 加入信号量机制，删除EXCEL 文件
@receiver(pre_delete, sender=ExcelStatus)
def ExcelStatus_delete(sender, instance, **kwargs):
    # print("[*] Deleting signal")
    if os.path.exists(instance.xl_file.path):
        os.remove(instance.xl_file.path)
    if os.path.exists(instance.pdf_file.path):
        os.remove(instance.pdf_file.path)
    if os.path.exists(instance.ans_file.path):
        os.remove(instance.ans_file.path)


class Words(models.Model):
    CN_TO_EN = (
        (1, "CN2EN"),
        (2, "EN2CN"),
        (0, "ALL ALLOW")
    )
    WorS = (
        (1, "Word"),
        (2, "Sentence")
    )
    en = models.CharField(max_length=400, null=False, blank=False, default=" ", verbose_name="英语",
                          help_text="en : 请在此输入英文")
    cn = models.CharField(max_length=400, null=False, blank=False, default=" ", verbose_name="中文",
                          help_text="cn : 请在此输入中文")
    comment = models.TextField(max_length=255, null=False, default=" ", verbose_name="备注",
                               help_text="comment : 请在此输入备注")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="创建日期")
    recite_time = models.DateTimeField(default=datetime(2000, 1, 1, 1, 1, 1, 1), verbose_name="背诵日期")
    recite_count = models.IntegerField(default=0, verbose_name="背诵次数")
    cn2en = models.SmallIntegerField(choices=CN_TO_EN, default=0, verbose_name="中翻英",
                                     help_text="cn2en : 1 代表中翻英，2代表英翻中，0（默认）代表都可以，系统会取随机数")
    word_or_sentence = models.SmallIntegerField(choices=WorS, default=1, verbose_name="单词还是句子",
                                                help_text="WorS(word_or_sentence) : 1(默认) 代表单词; 2 代表句子")
    enshrine_time = models.IntegerField(default=0, verbose_name="收藏次数", help_text="收藏一次单词,该数量自增1")
    file_source = models.ForeignKey(ExcelStatus, on_delete=models.DO_NOTHING, verbose_name="所属EXCEL文件",
                                    related_name="source")

    def __str__(self):
        return self.en + '\t' + self.cn
