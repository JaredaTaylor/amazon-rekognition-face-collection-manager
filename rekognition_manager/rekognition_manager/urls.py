"""rekognition_manager URL Configuration

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
# from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from faces import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    path('faces/', views.list_faces, name='list_faces'),
    path('faces/add/', views.add_face, name='add_face'),
    path('faces/delete/<str:face_id>/', views.delete_face, name='delete_face'),
]
