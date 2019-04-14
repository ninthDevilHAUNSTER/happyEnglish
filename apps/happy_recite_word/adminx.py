import xadmin
from .models import Words, ExcelStatus


class WordsAdmin(object):
    list_display = ["en", "cn",
                    "comment", 'recite_time', 'recite_count', 'cn2en']


class ExcelStatusAdmin(object):
    list_display = ['name', 'add_time', 'recite_time']


xadmin.site.register(Words, WordsAdmin)
xadmin.site.register(ExcelStatus, ExcelStatusAdmin)
