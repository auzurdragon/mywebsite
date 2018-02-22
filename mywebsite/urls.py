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
from mycoupon import views as mycoupon
from mychild import views as mychild
from mycms import views as cmsviews
from mynote import views as mynote
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.index),                # 指定首页为index
    url(r'^$', views.index),
    url(r'^coupon/$', mycoupon.tb_coupon),
    url(r'^mychild/practice/$', mychild.practice),
    url(r'^python/$', views.python),
    url(r'^examples/$', views.examples),
    url(r'^children/$', views.children),
    url(r'^syllabus/$', views.syllabus),
    url(r'^hwsubmit/$', views.hwsubmit),
    url(r'^booklist/$', views.booklist),
    url(r'^schedule/$', views.schedule),
    url(r'chisearch/$', views.chisearch),
    url(r'pinyin/$', views.pinyin),
    url(r'^login/$', views.login),
    url(r'^test/$', views.test),            # 返回request测试结果
    url(r'wxopen/$', views.wxopen),         # 微信接口验证
    url(r'wxopen$', views.wxopen),         # 微信接口验证，注意不能使用wxopen/$
    url(r'mycase/([\w.]{0,20})$', views.mycase),   # 传递()中的数字、字母和下划线字符给mycase()
    url(r'^applications/$', views.applications),  # 我的应用
    url(r'^mynote/weixin/$', mynote.weixin),        # 微信接口调用
    url(r'^mynote/weixin/login/$', mynote.weixin_login),    # 微信网页登录
    url(r'^mynote/weixin/check/$', mynote.weixin_check),
    # 管理后台
    url(r'cms/$', cmsviews.index),
    # root.txt文件验证，阿里
    url(r'root.txt', views.rootauth), 
    url(r'jos_guid.txt', views.jdrootcheck),    # 京东开发者网站验证
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
