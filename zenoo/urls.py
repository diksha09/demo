"""zenoo URL Configuration

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
from app1 import views as api_views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup', api_views.SignUpZenoUser, name='SignUpZenoUser'),
    path('login', api_views.LoginZenoUser, name='LoginZenoUser'),
    path('contactus', api_views.SendContactUsEmail, name='SendContactUsEmail'),
    path('logout', api_views.LogOutZenoUser, name='LogOutZenoUser'),
    path('addzenoadmin', api_views.addZenoAdmin, name='addZenoAdmin'),
    path('loginadmin', api_views.LoginZenoAdmin, name='LoginZenoAdmin'),
    path('addcategory', api_views.addCategory, name='addCategory'),
    path('additems', api_views.addItems, name='addItems'),
    path('addimages', api_views.addItemsImageAnsVideos, name='addItemsImageAnsVideos'),
    path('search', api_views.zenoSearch, name='zenoSearch'),
    path('userlist', api_views.getUserList, name='getUserList'),
    path('itemlist', api_views.getItemList, name='getItemList'),
    path('makeoffer', api_views.makeOffer, name='makeOffer'),
    path('sendmessage', api_views.sendMessage, name='sendMessage'),
    path('getmessage', api_views.getMessage, name='getMessage'),
    path('receivemessage', api_views.receiveMessage, name='receiveMessage'),
    path('getNotification', api_views.getNotification, name='getNotification'),
    path('shipperdetail', api_views.sendShipmentDetail, name='sendShipmentDetail'),
    path('deletemessage/<int:pk>', api_views.deteteMessage, name='deleteMessage'),
]
