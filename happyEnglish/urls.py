from django.contrib import admin
from django.urls import path
# version模块自动注册需要版本控制的 Model
import xadmin

xadmin.autodiscover()
from xadmin.plugins import xversion

xversion.register_models()

from happy_recite_word.views import index, word_import, word_output, gen_words_list, word_management, \
    del_excel_file, view_excel, enshrine_word, output_ans
from users.views import login, logout, register, user_info, page_not_found, bad_request
from django.conf.urls.static import static
from happyEnglish import settings

urlpatterns = [
                  path('admin/', xadmin.site.urls, name="admin"),
                  path('', index, name="home"),
                  path('import/', word_import, name="import"),
                  path('management/', word_management, name="management"),
                  path('enshrine_word/', enshrine_word, name='enshrine_word'),

                  path('api/ans_output/<int:id>', output_ans, name='ans_output'),
                  path('api/delete_excel/<int:id>', del_excel_file, name="delete_excel"),
                  path('api/view_excel/<int:id>', view_excel, name='view_excel'),
                  path('api/word_output/<int:id>', word_output, name="word_output"),
                  path('api/gen_words_list/<int:id>', gen_words_list, name='gen_words_list'),

                  path('user/login/', login, name="login"),
                  path('user/logout/', logout, name="logout"),
                  path('user/user_info/', user_info, name="user_info"),
                  path('user/register/', register, name="register")
              ] \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 如果部署生产环境请注释上行

handler404 = page_not_found
handler500 = bad_request
