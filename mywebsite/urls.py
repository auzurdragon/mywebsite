"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# 加载url解析方法, 用于urlpatterns
from django.conf.urls import url
# 加载admin, 用于管理后台url
from django.contrib import admin
# 加载静态文件目录
from django.conf import settings
from django.conf.urls.static import static
# 加载mywebsite下的views视图文件
from mywebsite import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index), # 指定首页为index
    url(r'^python/$', views.python),
    url(r'^examples/$', views.examples),
    url(r'^weixin/$', views.weixin),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
