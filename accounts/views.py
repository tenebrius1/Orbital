import datetime
import requests

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import Deliveries, Transaction


def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required(login_url='/accounts/login')
def dashboard(request):
    deliveries = Deliveries.objects.filter(user_id=request.user.id)
    context = {
        'deliveries': deliveries,
    }
    return render(request, "accounts/dashboard.html", context=context)


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
                messages.error(
                    request, "Account already created, please login instead.")
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

            user = auth.authenticate(
                request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid credentials")
                return redirect("login")
        else:
            return render(request, "accounts/login.html")


@login_required(login_url='/accounts/login')
def transaction(request):
    month = datetime.datetime.now()
    transactions = Transaction.objects.filter(user_id=request.user.id)
    context = {
        'month': month,
        'range': range(2),
        'transactions': transactions,
    }
    if request.method == "POST":
        name = request.POST["name"].lower()
        date = request.POST["date"]
        company = request.POST["company"]

        # Formats price to be in 2 decimal place
        price = request.POST["price"]
        price_formatted = float("{:.2f}".format(float(price)))

        # Formats date to be in the form of dd/mm/yyyy
        datelist = date.split("-")
        datelist.reverse()
        date = '{}/{}/{}'.format(*datelist)

        # Create and save new transaction
        Transaction.objects.create(
            item=name, user_id=request.user.id, date=date, price=price_formatted, company=company)

        return redirect("transaction")
    else:
        return render(request, "accounts/transaction.html", context=context)


@login_required(login_url='/accounts/login')
def price(request):
    return render(request, "accounts/price.html")


@login_required(login_url='/accounts/login')
def delivery(request):
    deliveries = Deliveries.objects.filter(user_id=request.user.id)
    context = {
        'deliveries': deliveries,
        'range': range(1),
    }

    if request.method == "POST":
        name = request.POST["name"].lower()
        tkg_number = request.POST["tkg_number"]
        courier_code = request.POST["courier"].split(",")[0]
        courier_name = request.POST["courier"].split(",")[1]
        Deliveries.objects.create(name=name, user_id=request.user.id, tkg_number=tkg_number,
                                  courier_code=courier_code, courier_name=courier_name)

        header = {
            "Content-Type": "application/json",
            "Tracking-Api-Key": "1468cec6-71f5-4cfe-9669-c9a80ef3705f",
        }

        params = {
            "tracking_number": tkg_number,
            "courier_code": courier_code,
        }

        r = requests.post(url="https://api.trackingmore.com/v3/trackings/realtime", headers=header, json=params)

        return redirect("delivery")
    else:
        return render(request, "accounts/delivery.html", context=context)


@login_required(login_url='/accounts/login')
def ship(request):
    return render(request, "accounts/ship.html")


# Handles AJAX Requests
def deleteTransaction(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item = request.POST.get("name").lower()
        date = request.POST.get("date")
        price = request.POST.get("price")[1:]
        company = request.POST.get("company")

        dlt = Transaction.objects.filter(
            item=item, date=date, price=price, company=company, user_id=request.user.id)[0]
        dlt.delete()

        return JsonResponse({"success": ""}, status=200)


def displayExpenses(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        transactions = Transaction.objects.filter(user_id=request.user.id)
        lazada = transactions.filter(company="Lazada").aggregate(
            Sum('price'))['price__sum']
        shopee = transactions.filter(company="Shopee").aggregate(
            Sum('price'))['price__sum']
        amazon = transactions.filter(company="Amazon").aggregate(
            Sum('price'))['price__sum']
        others = transactions.filter(company="Others").aggregate(
            Sum('price'))['price__sum']

        return JsonResponse({
            "lazada": lazada,
            "shopee": shopee,
            "amazon": amazon,
            "others": others,
        }, status=200)


def editTransaction(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        oItem = request.POST.get("oItem").lower()
        oDate = request.POST.get("oDate")
        oPrice = request.POST.get("oPrice")[1:]
        oCom = request.POST.get("oCom")
        oEntry = Transaction.objects.get(
            item=oItem, date=oDate, price=oPrice, company=oCom)

        oEntry.item = request.POST.get("nItem").lower()
        oEntry.date = request.POST.get("nDate")
        oEntry.price = float("{:.2f}".format(
            float(request.POST.get("nPrice"))))
        oEntry.company = request.POST.get("nCom")
        oEntry.save()

        return JsonResponse({"success": ""}, status=200)


def displayDeliveries(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Extract all tracking numbers
        deliveries = Deliveries.objects.filter(user_id=request.user.id)
        tkg_numbers = [delivery.tkg_number for delivery in deliveries]
        tracking_numbers = ""
        for number in tkg_numbers:
            tracking_numbers += number + ","

        header = {
            "Content-Type": "application/json",
            "Tracking-Api-Key": "1468cec6-71f5-4cfe-9669-c9a80ef3705f",
        }

        params = {
            "tracking_numbers": tracking_numbers
        }

        r = requests.get(
            url="https://api.trackingmore.com/v3/trackings/get", headers=header, params=params)

        return JsonResponse({
            "response": r.json()['data'],
        }, status=200)


def deleteDelivery(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        name = request.POST.get("name").lower()
        tkg_number = request.POST.get("tkg_number")

        dlt = Deliveries.objects.filter(name=name, tkg_number=tkg_number, user_id=request.user.id)[0]
        dlt.delete()

        return JsonResponse({"success": ""}, status=200)