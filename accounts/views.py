from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.shortcuts import redirect, render


def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def register(request):
    if request.method == 'POST':
        # Get form values
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Account already created, please login instead.")
            return
        else:
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            return redirect('index')

        return redirect('index')
