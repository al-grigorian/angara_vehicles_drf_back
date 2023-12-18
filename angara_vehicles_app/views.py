from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404 
from rest_framework import status 
from .serializers import * 
from .models import * 
from rest_framework.decorators import api_view
import datetime
from minio import Minio
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
# Create your views here.

# ----- Applications ----- 

# GET - получить список всех заявок (фильтр по дате формирования и статусу)
@api_view(['Get']) 
def get_applications(request, format=None):
    date_form = request.GET.get('date_form', datetime.datetime(2023, 9, 14, 18, 0, 0))
    status_param = request.GET.get('status', 1)
    applications = Applications.objects.filter(status=status_param) 
    serializer = ApplicationSerializer(applications, many=True) 
    return Response(serializer.data) 

#DELETE - удалить одну заявку
@api_view(['Delete']) 
def delete_application(request, pk, format=None):     
    application = get_object_or_404(Applications, pk=pk) 
    print(application.status)
    if application.status == '1':
        application.delete() 
        return Response("Заявка успешно удалена.")
    else:
        return Response("Невозможно изменить статус заявки. Текущий статус не равен 1.", status=status.HTTP_400_BAD_REQUEST)

#GET - получить одну заявку
@api_view(['GET'])
def get_application(request, pk, format=None):
    application = get_object_or_404(Applications, pk=pk)
    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        application_data = serializer.data

        # Получить связанные опции для заявки с полными данными из таблицы Components
        """
        application_options = ApplicationsComponents.objects.filter(id_application=application.pk)
        options_data = []
        for app_option in application_options:
            option_serializer = ComponentSerializer(app_option.id_component)
            option_data = option_serializer.data
            option_data['amount'] = app_option.amount
            options_data.append(option_data)
        
        # Добавить данные об опциях в данные о заявке
        application_data['options'] = options_data
        """
        return Response(application_data)

@api_view(["PUT"])
def update_by_user(request, pk):
    if not Applications.objects.filter(pk=pk).exists():
        return Response(f"Заявки с таким id не существует!")

    request_status = request.data["status"]

    if int(request.data["status"]) not in [2, 3]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    application = Applications.objects.get(pk=pk)
    app_status = application.status

    if int(request.data["status"]) in [3]:
        application.formation_date=timezone.now()
    

    application.status = request_status
    application.save()

    serializer = ApplicationSerializer(application, many=False)
    return Response(serializer.data)

@api_view(["PUT"])
def update_by_admin(request, pk):
    if not Applications.objects.filter(pk=pk).exists():
        return Response(f"Заявки с таким id не существует!")

    request_status = request.data["status"]

    if int(request.data["status"]) not in [4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    application = Applications.objects.get(pk=pk)
    if int(request.data["status"]) in [4]:
        application.completion_date=timezone.now()
    # app_status = application.status

    # if app_status == 5:
    #     return Response("Статус изменить нельзя")

    application.status = request_status
    application.save()

    serializer = ApplicationSerializer(application, many=False)
    return Response(serializer.data)

#DELETE - удалить конкретную опцию из конкретной заявки
@api_view(["DELETE"])
def delete_option_from_application(request, application_id, option_id):
    if not Applications.objects.filter(pk=application_id).exists():
        return Response("Заявки с таким id не существует", status=status.HTTP_404_NOT_FOUND)

    if not Components.objects.filter(pk=option_id).exists():
        return Response("Опции с таким id не существует", status=status.HTTP_404_NOT_FOUND)

    application = Applications.objects.get(pk=application_id)
    option = Components.objects.get(pk=option_id)

    ApplicationsComponents.objects.filter(id_component=option, id_application=application).delete()
    application.save()

    return Response("Опция успешно удалена из заявки", status=status.HTTP_204_NO_CONTENT)

#PUT - изменить кол-во конкретной опции в заявке
@api_view(["PUT"])
def update_option_amount(request, application_id, option_id):
    if not Applications.objects.filter(pk=application_id).exists() or not Components.objects.filter(pk=option_id).exists():
        return Response("Заявки или опции с такими id не существует", status=status.HTTP_404_NOT_FOUND)

    application_option = ApplicationsComponents.objects.filter(id_application=application_id, id_component=option_id).first()

    if not application_option:
        return Response("В этой заявке нет такой опции", status=status.HTTP_404_NOT_FOUND)

    new_amount = request.data.get("amount",1)
    application_option.components_amount = new_amount
    application_option.save()
    return Response("Amount успешно обновлен", status=status.HTTP_200_OK)
    # if new_amount is not None:

    # else:
    #     return Response("Неверные данные для обновления amount", status=status.HTTP_400_BAD_REQUEST)

# ----- Options -----

#GET - получить список всех опций (с фильтром)
@api_view(['Get']) 
def get_options(request, format=None): 
    
    search_query = request.GET.get('search', '')
    min_price = int(request.GET.get('min_price', 0))
    max_price = int(request.GET.get('max_price', 100000000))
    category = request.GET.get('category', '')
    print(search_query)

    components = Components.objects.filter(status=2).filter(component_name__icontains=search_query).filter(price__range=(min_price, max_price))
    
    if (category and category != 'Любая категория') :
        components = Components.filter(category=category)
    serializer = ComponentSerializer(components, many=True)

    return Response(serializer.data)

# GET - получить одну опцию
@api_view(['Get']) 
def get_option(request, pk, format=None): 
    option = get_object_or_404(Components, pk=pk) 
    if request.method == 'GET': 
        serializer = ComponentSerializer(option) 
        return Response(serializer.data)

#PUT - обновить опцию 
@api_view(['Put'])
def put_option(request, pk, format=None): 
    option = get_object_or_404(Components, pk=pk) 
    serializer = ComponentSerializer(option, data=request.data) 
    if serializer.is_valid(): 
        serializer.save() 
        return Response(serializer.data) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#PUT - удалить одну опцию
@api_view(['Put']) 
def delete_option(request, pk, format=None):
    if not Components.objects.filter(pk=pk).exists():
        return Response(f"Опции с таким id не существует!") 
    option = Components.objects.get(pk=pk)
    option.status = 1
    option.save()

    options = Components.objects.filter(status=2)
    serializer = ComponentSerializer(options, many=True)
    return Response(serializer.data)
    # return Response(status=status.HTTP_204_NO_CONTENT)

#POST - добавить опцию в заявку(если нет открытых заявок, то создать)
@api_view(['POST'])
def add_to_application(request, pk):
    if not Components.objects.filter(id=pk).exists():
        return Response(f"Опции с таким id не существует!")

    option = Components.objects.get(id=pk)

    application = Applications.objects.filter(status=1).last()

    if application is None:
        application = Applications.objects.create(id_creator=1)

    amount = request.data.get("amount", 1)
    try:
        application_option = ApplicationsComponents.objects.get(id_application=application.id, id_component=option.id)
        application_option.components_amount += int(amount)
        application_option.save()
    except ApplicationsComponents.DoesNotExist:
        application_option = ApplicationsComponents(id_application=application, id_component=option, components_amount=amount)
        application_option.save()

    return Response(status=200)

#POST - добавить новую опцию
@api_view(['Post']) 
def post_option(request, format=None):     
    serializer = ComponentSerializer(data=request.data) 
    if not serializer.is_valid(): 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    new_option = serializer.save() 
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
    client = Minio(endpoint="localhost:9000",
               access_key='minioadmin',
               secret_key='minioadmin',
               secure=False)
    i=new_option.id-1
    try:
        i = new_option.title
        img_obj_name = f"{i}.png"
        file_path = f"assets/img/{request.data.get('image')}"  
        client.fput_object(bucket_name='img',
                           object_name=img_obj_name,
                           file_path=file_path)
        new_option.image = f"http://localhost:9000/img/{img_obj_name}"
        new_option.save()
    except Exception as e:
        return Response({"error": str(e)})

# Используется для работы с Minio (подгрузка изображений в хранилище Minio)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def postImageToComponent(request, pk):
    print("Рлофывавы")
    if 'file' in request.FILES:
        file = request.FILES['file']
        component = Components.objects.get(pk=pk, status=2)
        
        client = Minio(endpoint="localhost:9000",
                       access_key='minioadmin',
                       secret_key='minioadmin',
                       secure=False)

        bucket_name = 'images'
        file_name = file.name
        file_path = "http://localhost:9000/images/" + file_name
        
        try:
            client.put_object(bucket_name, file_name, file, length=file.size, content_type=file.content_type)
            print("Файл успешно загружен в Minio.")
            
            serializer = ComponentSerializer(instance=component, data={'image_path': file_path}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse('Image uploaded successfully.')
            else:
                return HttpResponseBadRequest('Invalid data.')
        except Exception as e:
            print("Ошибка при загрузке файла в Minio:", str(e))
            return HttpResponseServerError('An error occurred during file upload.')

    return HttpResponseBadRequest('Invalid request.')