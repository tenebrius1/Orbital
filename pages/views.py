from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')

def signup(request):
    return render(request, 'pages/signup.html')
