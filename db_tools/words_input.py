__author__ = 'shaobao'

# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "happyEnglish.settings")

import django

django.setup()

from happyEnglish.settings import WORDS_ROOT, EXCEL_START_ROW_TITLE
from happy_recite_word.models import Words, ExcelStatus
import os

import xlrd
from datetime import datetime
import time
from happyEnglish.settings import MEDIA_ROOT


def import_excel():
    for root, dirs, files in os.walk(WORDS_ROOT):
        for file in files:
            if file.endswith(".xlsx") and not file.startswith("~"):
                file_path = root + file
                ExcelStatus.objects.update_or_create(
                    xl_name=file,
                    xl_path=file_path,
                    mod_time=datetime.fromtimestamp(os.stat(file_path).st_mtime),  # 文件的修改时间
                    add_time=datetime.fromtimestamp(os.stat(file_path).st_ctime)  # 文件的创建时间
                )


def import_data():
    for excel in ExcelStatus.objects.all():
        xl_path = excel.xl_path
        sheet = xlrd.open_workbook(xl_path).sheet_by_index(0)
        if sheet.nrows > 1:
            if sheet.row_values(0)[0:4] == EXCEL_START_ROW_TITLE:
                for row_id in range(1, sheet.nrows):
                    row_value = sheet.row_values(row_id)[0:4]
                    Words.objects.update_or_create(
                        file_source=excel,
                        en_word=row_value[0],
                        en_verse=row_value[1],
                        cn_word=row_value[2],
                        comment=row_value[3]
                    )


import csv


def handle_excel_file(id):
    excel = ExcelStatus.objects.filter(id=id)[0]
    file_relative_path = excel.xl_file.__str__()
    if file_relative_path.endswith('xlsx'):
        xlsx = xlrd.open_workbook(MEDIA_ROOT + "\\" + file_relative_path).sheet_by_index(0)
        if xlsx.nrows > 1:
            if xlsx.row_values(0)[0:5] == EXCEL_START_ROW_TITLE:
                pass
            else:
                return False, "EXCEL 头行参数不正确"
            for row_id in range(1, xlsx.nrows):
                row_value = xlsx.row_values(row_id)[0:5]
                print(row_value)
                Words.objects.update_or_create(
                    file_source=excel,
                    en=row_value[0],
                    cn=row_value[1],
                    cn2en=int(row_value[2]),
                    word_or_sentence=int(row_value[3]),
                    comment=row_value[4]
                )
            return True, '数据传输成功'
        else:
            return False, "EXCEL 为空文件"


    elif file_relative_path.endswith('csv'):
        with open(MEDIA_ROOT + "\\" + file_relative_path, 'r', encoding='utf8') as f:
            # csv_file = csv.DictReader(f)
            csv_file = csv.reader(f)
            for row_value in csv_file:
                if csv_file.line_num == 1:
                    if row_value[0:5] == EXCEL_START_ROW_TITLE:
                        pass
                    else:
                        return False, "CSV 头行参数不正确"
                else:
                    Words.objects.update_or_create(
                        file_source=excel,
                        en=row_value[0],
                        cn=row_value[1],
                        cn2en=int(row_value[2]),
                        word_or_sentence=int(row_value[3]),
                        comment=row_value[4]
                    )
            return True, '数据传输成功'
    else:
        return False, "Hello hacker"
