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
from api import views as api
from myapps import views as myapps
# 加载重定向模块
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.index),                  # 指定首页为index
    url(r'^$', mycoupon.tb_coupon),
    url(r'^myapps/$', myapps.myapps),           # 加载我的应用首页
    url(r'^myapps/qydata/$', myapps.qydata),
    url(r'^myapps/wordcloud/$', myapps.wordcloud),
    url(r'^favicon.ico$', RedirectView.as_view(url='static/favicon.ico')),  # 返回favicon.ico
    url(r'^coupon/$', mycoupon.tb_coupon),
    url(r'^coupon/coupon_rest', mycoupon.coupon_rest),
    # url(r'^mynote/$', mynote.index),        # 加载mynote主页
    url(r'^api/weixin', api.weixin),        # 加载微信api
    url(r'^sitelog/$', views.sitelog),    # 网站更新日志
    # url(r'^mychild/practice/$', mychild.practice),
    url(r'^examples/$', views.examples),
    url(r'^syllabus/$', views.syllabus),
    url(r'^login/$', views.login),
    # url(r'^test/$', views.test),            # 返回request测试结果
    # url(r'wxopen/$', views.wxopen),         # 微信接口验证
    # url(r'wxopen$', views.wxopen),         # 微信接口验证，注意不能使用wxopen/$
    url(r'mycase/([\w.]{0,20})$', views.mycase),   # 传递()中的数字、字母和下划线字符给mycase()
    # 管理后台
    # url(r'cms/$', cmsviews.index),
    url(r'root.txt', views.rootauth),             # root.txt文件验证，阿里www.4zan.net/root.txt
    # url(r'jos_guid.txt', views.jdrootcheck),      # 京东开发者网站验证
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
