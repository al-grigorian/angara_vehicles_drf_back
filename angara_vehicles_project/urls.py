from django.contrib import admin
from django.urls import path
 
from django.contrib import admin
from angara_vehicles_app import views
from django.urls import include, path
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from rest_framework import permissions
from rest_framework import routers

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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

    path('create/',  views.create, name='create'),
    path('login/',  views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_info/', views.user_info, name='user_info'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]