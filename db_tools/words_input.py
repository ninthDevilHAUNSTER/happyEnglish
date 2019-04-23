__author__ = 'shaobao'

# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "happyEnglish.settings")

import django

django.setup()

from happyEnglish.settings import EXCEL_START_ROW_TITLE
from happy_recite_word.models import Words, ExcelStatus
import os

import xlrd
from datetime import datetime
from happyEnglish.settings import MEDIA_ROOT
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
                Words.objects.update_or_create(
                    file_source=excel,
                    en=row_value[0],
                    cn=row_value[1],
                    cn2en=int(row_value[2]) if row_value[2] != "" else 0,
                    word_or_sentence=int(row_value[3]) if row_value[3] != "" else 1,
                    comment=row_value[4]
                )
            return True, '数据传输成功'
        else:
            return False, "EXCEL 为空文件"


    elif file_relative_path.endswith('csv'):
        with open(MEDIA_ROOT + "\\" + file_relative_path, 'r', encoding='utf8') as f:
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
                        cn2en=int(row_value[2]) if row_value[2] != "" else 0,
                        word_or_sentence=int(row_value[3]) if row_value[3] != "" else 1,
                        comment=row_value[4]
                    )
            return True, '数据传输成功'
    else:
        return False, "Hello hacker"
