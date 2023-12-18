"""
URL configuration for angara_vehicles_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from angara_vehicles_app import views
from rest_framework import permissions

router = routers.DefaultRouter()

urlpatterns = [
    # OPTIONS

    path('', include(router.urls)),
    path(r'options/', views.get_options, name='options-list'),#GET - получить список всех опций - ок
    path(r'options/post/', views.post_option, name='options-post'),#POST - добавить новую опцию - ?
    path(r'options/<int:pk>/', views.get_option, name='options-detail'),#GET - получить одну  - ок
    path(r'options/<int:pk>/put/', views.put_option, name='options-put'),#PUT - обновить одну опцию - ок
    path(r'options/<int:pk>/delete/', views.delete_option, name='options-delete'),#PUT - удалить одну опцию - ок
    path(r'options/<int:pk>/add_to_application/', views.add_to_application, name='options-add-to-application'),#POST - добавить опцию в заявку(если нет открытых заявок, то создать) - ок
    path(r'options/<int:pk>/image/post/', views.postImageToComponent, name="post-image-to-component"), #POST - добавление картинки в хранилище Minio - ?
    
    # APPLICATIONS
    
    path(r'applications/', views.get_applications, name='applications-list'),# GET - получить список всех заявок (фильтр по дате формирования и статусу) - ок
    path(r'applications/<int:pk>/', views.get_application, name='applications-detail'),#GET - получить одну заявку (без списка услуг внутри) - ок
    path(r'applications/<int:pk>/delete/', views.delete_application),#DELETE - удалить одну заявку - ок
    path(r'applications/<int:pk>/update_by_user/', views.update_by_user, name='update_by_user'),#PUT - изменение статуса пользователем - ок
    path(r'applications/<int:pk>/update_by_admin/', views.update_by_admin, name='update_by_admin'),#PUT - изменение статуса модератором - ок

    path(r"applications/<int:application_id>/delete_option/<int:option_id>/", views.delete_option_from_application),#DELETE - удалить конкретную опцию из конкретной заявки - ок
    path(r"applications/<int:application_id>/update_amount/<int:option_id>/", views.update_option_amount),#PUT - изменить кол-во конкретной опции в заявке - ок

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]