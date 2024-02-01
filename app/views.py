import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_order(request):
    user = identity_user(request)

    if user is None:
        return None

    order = Order.objects.filter(owner_id=user.pk).filter(status=1).first()

    if order is None:
        return None

    return order


@api_view(["GET"])
def search_vehicles(request):
    query = request.GET.get("component", "")

    vehicles = Vehicle.objects.filter(status=1).filter(name__icontains=query)

    serializer = VehicleSerializer(vehicles, many=True)

    draft_order = get_draft_order(request)

    resp = {
        "vehicles": serializer.data,
        "draft_order_id": draft_order.pk if draft_order else None
    }

    return Response(resp)


@api_view(["GET"])
def get_vehicle_by_id(request, component_id):
    if not Vehicle.objects.filter(pk=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vehicle = Vehicle.objects.get(pk=component_id)
    serializer = VehicleSerializer(vehicle)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_vehicle(request, component_id):
    if not Vehicle.objects.filter(pk=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vehicle = Vehicle.objects.get(pk=component_id)
    serializer = VehicleSerializer(vehicle, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_vehicle(request):
    vehicle = Vehicle.objects.create()

    serializer = VehicleSerializer(vehicle)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_vehicle(request, component_id):
    if not Vehicle.objects.filter(pk=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vehicle = Vehicle.objects.get(pk=component_id)
    vehicle.status = 5
    vehicle.save()

    vehicles = Vehicle.objects.filter(status=1)
    serializer = VehicleSerializer(vehicles, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_vehicle_to_order(request, component_id):
    if not Vehicle.objects.filter(pk=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vehicle = Vehicle.objects.get(pk=component_id)

    draft_order = get_draft_order(request)

    if draft_order is None:
        draft_order = Order.objects.create()
        draft_order.owner = identity_user(request)
        draft_order.save()

    if VehicleOrder.objects.filter(order=draft_order, vehicle=vehicle).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = VehicleOrder.objects.create()
    cons.order = draft_order
    cons.vehicle = vehicle
    cons.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_vehicle_image(request, component_id):
    if not Vehicle.objects.filter(pk=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vehicle = Vehicle.objects.get(pk=component_id)

    return HttpResponse(vehicle.image, content_type="image/png")

"""
@api_view(["PUT"])
@permission_classes([IsModerator])
def update_vehicle_image(request, component_id):
    if not Vehicle.objects.filter(pk=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    vehicle = Vehicle.objects.get(pk=component_id)
    serializer = VehicleSerializer(vehicle, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
"""

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_orders(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    orders = Order.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        orders = orders.filter(owner_id=user.pk)

    if status_id != -1:
        orders = orders.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        orders = orders.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        orders = orders.filter(date_formation__lte=parse_datetime(date_end))

    serializer = OrdersSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, rocket_id):
    if not Order.objects.filter(pk=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=rocket_id)
    serializer = OrderSerializer(order)

    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order(request, rocket_id):
    if not Order.objects.filter(pk=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=rocket_id)
    serializer = OrderSerializer(order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_weight(request, rocket_id):
    if not Order.objects.filter(pk=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=rocket_id)
    serializer = OrderSerializer(order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, rocket_id):
    if not Order.objects.filter(pk=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=rocket_id)

    order.owner = identity_user(request)
    order.status = 2
    order.date_formation = timezone.now()
    order.save()

    calculate_weight(rocket_id)

    serializer = OrderSerializer(order)

    return Response(serializer.data)


def calculate_weight(order_id):
    data = {
        "order_id": order_id
    }

    requests.post("http://127.0.0.1:8080/calc_weight/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, rocket_id):
    if not Order.objects.filter(pk=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=rocket_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.moderator = identity_user(request)
    order.status = request_status
    order.date_complete = timezone.now()
    order.save()

    serializer = OrderSerializer(order)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, rocket_id):
    if not Order.objects.filter(pk=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=rocket_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 5
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_vehicle_from_order(request, rocket_id, component_id):
    if not VehicleOrder.objects.filter(order_id=rocket_id, vehicle_id=component_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = VehicleOrder.objects.get(order_id=rocket_id, vehicle_id=component_id)
    item.delete()

    if not VehicleOrder.objects.filter(order_id=rocket_id).exists():
        order = Order.objects.get(pk=rocket_id)
        order.delete()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_vehicle_in_order(request, rocket_id, component_id):
    if not VehicleOrder.objects.filter(vehicle_id=component_id, order_id=rocket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = VehicleOrder.objects.get(vehicle_id=component_id, order_id=rocket_id)

    serializer = VehicleOrderSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {
            "message": "Введенные данные невалидны"
        }
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    serializer = UserCheckSerializer(
        user,
        context={
            "access_token": access_token
        }
    )

    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован',
        'user_id': user.id,
        "access_token": access_token
    }

    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def check(request):
    user = identity_user(request)

    user = CustomUser.objects.get(pk=user.pk)
    serializer = UserCheckSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {
        "message": "Вы успешно вышли из аккаунта"
    }

    return Response(message, status=status.HTTP_200_OK)
