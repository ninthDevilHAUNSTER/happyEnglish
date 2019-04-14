"""happyEnglish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# version模块自动注册需要版本控制的 Model
import xadmin

xadmin.autodiscover()
from xadmin.plugins import xversion

xversion.register_models()

from happy_recite_word import views

urlpatterns = [
    path('admin/', xadmin.site.urls, name="admin"),
    path('', views.index, name="home"),
    path('import/', views.word_import, name="import"),
    path('output/', views.word_output, name="output"),
    path('gen_words_list/<int:id>',views.gen_words_list,name='gen_words_list'),
    path('management/', views.word_management, name="management"),
    path('delete_excel/<int:id>', views.del_excel_file, name="delete_excel"),
    path('view_excel/<int:id>', views.view_excel, name='view_excel'),
    # path('update_time/<int:id>',views.update_time,name='update_time')
]

handler404 = views.page_not_found
handler500 = views.bad_request
