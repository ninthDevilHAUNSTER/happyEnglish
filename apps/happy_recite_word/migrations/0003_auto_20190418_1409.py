# Generated by Django 2.0.13 on 2019-04-18 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happy_recite_word', '0002_excelstatus_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='cn',
            field=models.CharField(default=' ', help_text='cn : 请在此输入中文', max_length=400, verbose_name='中文'),
        ),
        migrations.AlterField(
            model_name='words',
            name='en',
            field=models.CharField(default=' ', help_text='en : 请在此输入英文', max_length=400, verbose_name='英语'),
        ),
    ]
