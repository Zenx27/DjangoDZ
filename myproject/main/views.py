import requests
from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def api_data(request):
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = response.json()
    return render(request, 'main/api_data.html', {'users': users})
