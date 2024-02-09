from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect  
from .models import * 
import psycopg2

connection = psycopg2.connect(dbname="angara_vehicles_assembly", host="localhost", user="postgres", password="psadeiw123", port="5433")
cursor = connection.cursor()
# Create your views here.


def GetOptions(request):
    input_text = request.GET.get('rocketcopm')
    options=Components.objects.filter(status__exact=2)
    #context={'vars': options}
    if input_text:
        filtered_options = Components.objects.filter(category__icontains=input_text).filter(status=2)
        return render(request, 'main_page.html', {'data' : {
        'result': filtered_options, 'find': input_text
    }})
    else:
        return render(request, 'main_page.html', {'data' : {
        'result': options
    }})

def GetOption(request, id): 
    result = Components.objects.get(id=id)
    return render(request, 'rocket_page.html', {'data' : {
        'result': result
    }}) 

def DeleteRecord(request, record_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE angara_vehicles_app_components SET status=1 WHERE id = %s", (record_id,))
        connection.commit()
        cursor.close()
    return redirect('options_url')