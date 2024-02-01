from rest_framework import serializers

from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    def get_amount(self, vehicle):
        return self.context.get("amount", "")

    class Meta:
        model = Vehicle
        fields = "__all__"


class UserCheckSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    def get_access_token(self, user):
        return self.context.get("access_token", "")

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator', 'access_token')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name')


class OrderSerializer(serializers.ModelSerializer):
    vehicles = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_vehicles(self, order):
        items = VehicleOrder.objects.filter(order_id=order.pk)

        vehicles = []
        for item in items:
            serializer = VehicleSerializer(
                item.vehicle,
                context={
                    "amount": item.amount
                }
            )
            vehicles.append(serializer.data)


        return vehicles

    class Meta:
        model = Order
        fields = "__all__"


class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name')


class OrdersSerializer(serializers.ModelSerializer):
    owner = OrderUserSerializer(read_only=True, many=False)
    moderator = OrderUserSerializer(read_only=True, many=False)

    class Meta:
        model = Order
        fields = "__all__"


class VehicleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleOrder
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


