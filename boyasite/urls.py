"""boyasite URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from main import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls')),

    url(r'^article/', views.article),
    url(r'^article_input/', views.article_input),
    url(r'^test/', views.test),
    url(r'^show_detail/', views.show_detail),
    url(r'^delete/', views.delete),

    url(r'^visit/', views.visit),
    url(r'^visit_show\d*/', views.visit_show),
    url(r'^search/',views.search),
    url(r'^sport/', views.sport),
    url(r'^sport_show/', views.sport_show),
    url(r'^profile', views.profile),
    url(r'^change_password', views.change_password),
    url(r'^volunteer', views.volunteer),
    url(r'^volunteer_show', views.volunteer_show),
]
