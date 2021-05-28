from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
import datetime

def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required(login_url='/accounts/login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        if request.method == "POST":
            # Get form values
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]

            # Check email
            if User.objects.filter(email=email).exists():
                messages.error(request, "Account already created, please login instead.")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username has already been taken.")
                return redirect("register")
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )
                # Login User after they register
                auth.login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                return redirect("dashboard")

                # Redirect user to login page after registration
                # user.save()
                # return redirect("login")
        else:
            return render(request, "accounts/register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid credentials")
                return redirect("login")
        else:
            return render(request, "accounts/login.html")

def transaction(request):
    month = datetime.datetime.now()
    context = {
        'month': month,
        'range': range(8)
    }
    if request.method == "POST":
        name = request.POST["name"]
        date = request.POST["date"]
        company = request.POST["company"]
        price = request.POST["price"]
        request.session['item']= {
            'name': name,
            'date': date,
            'company': company,
            'price': price,
        }
        return redirect("transaction")
    else: 
        return render(request, "accounts/transaction.html", context=context)

def price(request):
    return render(request, "accounts/price.html")

def delivery(request):
    return render(request, "accounts/delivery.html")

def ship(request):
    return render(request, "accounts/ship.html")
