import datetime

import requests
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from environs import Env
from scraping.checkPrice import checkPrice
from scraping.models import Price

from .models import Deliveries, Transaction, Shipping, Group

# Set up environ
env = Env()
env.read_env()

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
    entries = Price.objects.filter(user_id=request.user.id)
    context = {
        'entries': entries,
    }

    if request.method == "POST":
        name = request.POST["name"]
        url = request.POST["url"]
        company = request.POST["company"]

        # first scrape
        price = checkPrice(url)
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        Price.objects.create(name=name, user_id=request.user.id,
                             url=url, company=company, priceArr=[price], dateArr=[date])

        return redirect("price")
    else:
        return render(request, "accounts/price.html", context=context)

@login_required(login_url='/accounts/login')
def delivery(request):
    deliveries = Deliveries.objects.filter(user_id=request.user.id)
    context = {
        'deliveries': deliveries,
        'range': range(1),
    }

    if request.method == "POST":
        name = request.POST["name"]
        tkg_number = request.POST["tkg_number"]
        courier_code = request.POST["courier"].split(",")[0]
        courier_name = request.POST["courier"].split(",")[1]
        Deliveries.objects.create(name=name, user_id=request.user.id, tkg_number=tkg_number,
                                  courier_code=courier_code, courier_name=courier_name)

        header = {
            "Content-Type": "application/json",
            "Tracking-Api-Key": env.str('TRACKING_API_KEY'),
        }

        params = {
            "tracking_number": tkg_number,
            "courier_code": courier_code,
        }

        requests.post(
            url="https://api.trackingmore.com/v3/trackings/realtime", headers=header, json=params)

        return redirect("delivery")
    else:
        return render(request, "accounts/delivery.html", context=context)

@login_required(login_url='/accounts/login')
def ship(request):
    if request.method == "POST":
        name = request.POST["name"]
        platform = request.POST["platform"]
        location = request.POST["location"]
        contact = request.POST['contact']
        base_shipping = request.POST['base_shipping_fee']
        free_shipping_min = request.POST['freeshipping']
        description = request.POST['description']
        owner = request.user.username

        grp = Group.objects.create(
            group_name=name, description=description, members=[owner], contacts=[contact], owner=owner)
        Shipping.objects.create(group=grp, group_name=name, platform=platform, location=location,
                                base_shipping=base_shipping, free_shipping_min=free_shipping_min, member_count=1)
        
        return redirect(f'ship/{name}')
    else:
        groups = Shipping.objects.all()
        mygroups = Group.objects.filter(members__contains=[request.user.username])
        context = {
            'groups': groups,
            'mygroups': mygroups,
        }
        return render(request, "accounts/ship.html", context)

def deleteGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        grp = Group.objects.get(pk=group_name)
        grp.delete()
        grp_ship = Shipping.objects.get(pk=group_name)
        grp_ship.delete()
        return JsonResponse({"success": ""}, status=200)

def joinGroup(request):
    if request.method == 'POST':
        contact = request.POST['contact']
        group_name = request.POST['group_name']
        grp = Group.objects.get(pk=group_name)
        group_shipping = Shipping.objects.get(pk=group_name)
        grp.members.append(request.user.username)
        grp.contacts.append(contact)
        grp.save()
        group_shipping.member_count += 1
        group_shipping.save()
        return redirect(f'ship/{group_name}')

def leaveGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        grp = Group.objects.get(pk=group_name)
        grp_shipping = Shipping.objects.get(pk=group_name)
        index = grp.members.index(request.user.username)
        grp.contacts.pop(index)
        grp.members.remove(request.user.username)
        grp.save()
        grp_shipping.member_count -= 1
        grp_shipping.save()
        return JsonResponse({"success": ""}, status=200)

def lockGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        print(group_name)
        grp = Group.objects.get(pk=group_name)
        grp.is_locked = True
        grp.save()
        return JsonResponse({"success": ""}, status=200)

def groupmainpage(request, group_name):
    context = {
        'info': Group.objects.filter(group_name=group_name)[0],
        'shipping': Shipping.objects.filter(group_name=group_name)[0]
    }
    if request.method == 'POST':
        return redirect('groupmainpage', group_name=group_name)
    else:
        return render(request, "accounts/groupmainpage.html", context)

def grouplocked(request, group_name):
    context = {
        'info': Group.objects.filter(group_name=group_name)[0],
        'shipping': Shipping.objects.filter(group_name=group_name)[0],
    }
    if request.method == "POST":
        return
    else:    
        return render(request, "accounts/grouplocked.html", context)

@login_required(login_url='/accounts/login')
def settings(request):
    u = User.objects.get(username=request.user.username)
    if request.method == "POST":
        # Get form values
        username = request.POST["newname"]
        password = request.POST["newpw"]

        u.set_password(password)
        u.save()

        auth.login(
            request, u, backend="django.contrib.auth.backends.ModelBackend"
        )

        return redirect("settings")

        # Redirect user to login page after registration
        # user.save()
        # return redirect("login")
    else:
        return render(request, "accounts/settings.html")


def forgetpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        # Check email
        if User.objects.filter(email=email).exists() == False:
            messages.error(
                request, "Email does not exist.")
            return redirect("forgetpassword")
        else:
            return redirect("resetpasswordsuccess")

    return render(request, "accounts/forgetpassword.html")


def resetpasswordsuccess(request):
    return render(request, "accounts/resetpasswordsuccess.html")

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
            "Tracking-Api-Key": env.str('TRACKING_API_KEY'),
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
        name = request.POST.get("name")
        tkg_number = request.POST.get("tkg_number")

        dlt = Deliveries.objects.filter(
            name=name, tkg_number=tkg_number, user_id=request.user.id)[0]
        dlt.delete()

        return JsonResponse({"success": ""}, status=200)