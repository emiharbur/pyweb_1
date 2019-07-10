"""pyweb_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
from sqlweb import views as sqlweb_view
from django.views import static
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', sqlweb_view.index),
    path('login/',sqlweb_view.login_v),
    path('logout/',sqlweb_view.logout_v),
    path('additem/<sort>/',sqlweb_view.additem),
    path('additem/<sort>/itemsave/',sqlweb_view.itemsave),
    path('itemsave/', sqlweb_view.itemsave),
    path('item/',sqlweb_view.item_v),
    path('applicationsave/',sqlweb_view.applicationsave),
    path('viewapplication/',sqlweb_view.viewapplication),
    path('applicationreject/',sqlweb_view.applicationreject),
    path('applicationapprove/',sqlweb_view.applicationapprove),
    path('subjecttable/', sqlweb_view.subject_v),
    path('addsubject/', sqlweb_view.addsubject),
    path('subjectsave/', sqlweb_view.subjectsave),
    path('payview/', sqlweb_view.payview),
    path('paydetail/<appid>', sqlweb_view.paydetail),
    path('paydetail/paycheck/<appid>', sqlweb_view.paycheck),



    re_path(r'^itemdetail/(?P<itemid>[0-9]{10})/$', sqlweb_view.item_detail),
    re_path(r'^applicationdetail/(?P<applicationid>[0-9]{11})/$', sqlweb_view.application_detail),
    path('subjectdetail/<subjectid>/', sqlweb_view.subjectdetail),


    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]
