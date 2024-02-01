from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/components/search/', search_vehicles),  # GET
    path('api/components/<int:component_id>/', get_vehicle_by_id),  # GET
    path('api/components/<int:component_id>/image/', get_vehicle_image),  # GET
    path('api/components/<int:component_id>/update/', update_vehicle),  # PUT
    #path('api/components/<int:component_id>/update_image/', update_vehicle_image),  PUT
    path('api/components/<int:component_id>/delete/', delete_vehicle),  # DELETE
    path('api/components/create/', create_vehicle),  # POST
    path('api/components/<int:component_id>/add_to_rocket/', add_vehicle_to_order),  # POST

    # Набор методов для заявок
    path('api/rockets/search/', search_orders),  # GET
    path('api/rockets/<int:rocket_id>/', get_order_by_id),  # GET
    path('api/rockets/<int:rocket_id>/update/', update_order),  # PUT
    path('api/rockets/<int:rocket_id>/update_weight/', update_weight),  # PUT
    path('api/rockets/<int:rocket_id>/update_status_user/', update_status_user),  # PUT
    path('api/rockets/<int:rocket_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/rockets/<int:rocket_id>/delete/', delete_order),  # DELETE

    # м-м
    path('api/rockets/<int:rocket_id>/update_component/<int:component_id>/', update_vehicle_in_order),  # PUT
    path('api/rockets/<int:rocket_id>/delete_component/<int:component_id>/', delete_vehicle_from_order),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]
