import datetime

import cloudinary
import requests
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    password_validators_help_texts, validate_password)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from environs import Env

from .models import Data, Deliveries, Group, Shipping, Transaction, UserExtension
from .utils import account_activation_token

# Set up environ
env = Env()
env.read_env()

# Cloudinary config
cloudinary.config(
    cloud_name=env.str('CLOUD_NAME'),
    api_key=env.str('API_KEY'),
    api_secret=env.str('API_SECRET'),
    secure=True
)


def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required(login_url='/accounts/login')
def dashboard(request):
    mygroups = Group.objects.filter(members__contains=[request.user.username])
    user = UserExtension.objects.filter(user=request.user)
    platform = list()
    for i in range(len(mygroups)):
        g = Shipping.objects.filter(group_name=mygroups[i].group_name)
        platform.append(g[0].platform)
    deliveries = Deliveries.objects.filter(user_id=request.user.id)
    expense = Transaction.objects.filter(user_id=request.user.id)

    first_time = True
    if len(user) == 0 or not user[0].first_time_user:
        first_time = False

    context = {
        'deliveries': deliveries if len(deliveries) != 0 else None,
        'mygroups': zip(mygroups, platform) if len(mygroups) != 0 else None,
        'first_time': first_time,
        'transactions': True if len(expense) != 0 else False,
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

            try:
                validate_password(password)
            except:
                messages.error(request, password_validators_help_texts(password_validators=None))
                return redirect("register")

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
                user.is_active = False
                user.save()
                current_site = get_current_site(request).domain
                email_body = {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://shopbud.herokuapp.com'+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+ user.username + ', Please click the link below to activate your account \n'+ activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)

                UserExtension.objects.create(user=user, first_time_user=True)

                messages.success(request, 'An email has been sent to you to activate your account')
                return redirect("register")
        else:
            return render(request, "accounts/register.html")

def activate(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not account_activation_token.check_token(user, token):
            messages.error(request, 'User already active')
            return redirect('login')

        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')

    except Exception:
        pass

    return redirect('login')

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
                if not User.objects.get(username=username).is_active:
                    messages.error(request, 'Account is not active, please check your email')
                    return redirect("login")
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
def delivery(request):
    deliveries = Deliveries.objects.filter(user_id=request.user.id)
    context = {
        'deliveries': deliveries,
    }

    if request.method == "POST":
        name = request.POST["name"].lower()
        tkg_number = request.POST["tkg_number"]
        courier_code = request.POST["courier"].split(",")[0]
        courier_name = request.POST["courier"].split(",")[1]

        header = {
            "Content-Type": "application/json",
            "Tracking-Api-Key": env.str('TRACKING_API_KEY'),
        }

        params = {
            "tracking_number": tkg_number,
            "courier_code": courier_code,
        }

        r = requests.post(
            url="https://api.trackingmore.com/v3/trackings/realtime", headers=header, json=params)
        
        if r.json()["data"]["delivery_status"] == "notfound":
            messages.error(request, " ")
            return redirect("delivery")
        else:
            Deliveries.objects.create(name=name, user_id=request.user.id, tkg_number=tkg_number,
                                  courier_code=courier_code, courier_name=courier_name)
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
        user = UserExtension.objects.filter(user=request.user)

        if len(user) != 0:
            user[0].phone_number = contact
            user[0].save()
        else:
            UserExtension.objects.create(user=User.objects.get(user_id=request.user.id), phone_number=contact)

        return redirect(f'ship/{name}')
    else:
        groups = Shipping.objects.all()
        mygroups = Group.objects.filter(
            members__contains=[request.user.username])
        user = UserExtension.objects.filter(user=request.user)
        context = {
            'groups': groups,
            'mygroups': mygroups,
            'contact': user[0].phone_number if len(user) != 0 else ''
        }
        return render(request, "accounts/ship.html", context)


def joinGroup(request):
    if request.method == 'POST':
        contact = request.POST['contact']
        group_name = request.POST['group_name']
        grp = Group.objects.get(pk=group_name)
        user = UserExtension.objects.filter(user=request.user)
        group_shipping = Shipping.objects.get(pk=group_name)
        grp.members.append(request.user.username)
        grp.contacts.append(contact)
        grp.save()
        group_shipping.member_count += 1
        group_shipping.save()

        if len(user) != 0:
            user[0].phone_number = contact
            user[0].save()
        else:
            UserExtension.objects.create(user=User.objects.get(user_id=request.user.id), phone_number=contact)

        return redirect(f'ship/{group_name}')


@login_required(login_url='/accounts/login')
def groupmainpage(request, group_name):
    group = Group.objects.get(group_name=group_name)
    data = Data.objects.filter(group_name=group_name)
    user = UserExtension.objects.filter(user=request.user)
    # Ensures that the group is locked before allowing members to access this page
    # if group.is_locked:
    #     return redirect('grouplocked', group_name=group_name)
    tabledata = None
    if len(data) != 0:
        tabledata = zip(data[0].users, data[0].items,
                        data[0].quantity, data[0].prices, data[0].urls)
    context = {
        'info': group,
        'shipping': Shipping.objects.filter(group_name=group_name)[0],
        'data': data[0] if len(data) != 0 else None,
        'table_data': tabledata,
        'contact': user[0].phone_number if len(user) != 0 else ''
    }
    if request.method == 'POST':
        user = request.user.username
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        url = request.POST['url']
        adddata = None
        if len(data) == 0:
            if request.user.username == group.owner:
                adddata = Data.objects.create(group_name=group, users=[user], items=[name], prices=[
                                              price], urls=[url], quantity=[quantity], paid=[True])
            else:
                adddata = Data.objects.create(group_name=group, users=[user], items=[name], prices=[
                                              price], urls=[url], quantity=[quantity], paid=[False])
            adddata.save()
        else:
            adddata = Data.objects.filter(group_name=group)[0]
            adddata.users.append(user)
            adddata.items.append(name)
            adddata.prices.append(price)
            adddata.urls.append(url)
            adddata.quantity.append(quantity)
            adddata.paid.append(
                False if request.user.username != group.owner else True)
            adddata.save()
        return redirect('groupmainpage', group_name=group_name)
    else:
        return render(request, "accounts/groupmainpage.html", context)


@login_required(login_url='/accounts/login')
def grouplocked(request, group_name):
    group = Group.objects.get(group_name=group_name)
    data = Data.objects.filter(group_name=group)
    user_total = 0

    # Ensures that the group is locked before allowing members to access this page
    # if not group.is_locked:
    #     return redirect('groupmainpage', group_name=group_name)

    tabledata = None
    if len(data) != 0:
        tabledata = zip(data[0].users, data[0].items, data[0].quantity,
                        data[0].prices, data[0].urls, data[0].paid)
        for i in range(len(data[0].users)):
            if data[0].users[i] == request.user.username:
                user_total += data[0].prices[i] * data[0].quantity[i]

    context = {
        'info': group,
        'shipping': Shipping.objects.filter(group_name=group_name)[0],
        'member_details': zip(group.members, group.contacts),
        'table_data': tabledata,
        'date': group.meeting_date.isoformat(),
        'user_total': user_total,
    }
    if request.method == "POST":
        tkg_number = request.POST['tkg_number']
        courier = request.POST['courier']
        meetup = request.POST['date']
        date = datetime.date.fromisoformat(meetup)
        address = request.POST['address']

        group.tkg_number = tkg_number
        group.courier = courier
        group.address = address
        group.meeting_date = date
        group.save()

        return redirect('grouplocked', group_name=group_name)
    else:
        return render(request, "accounts/grouplocked.html", context)


def uploadImage(request):
    if request.method == 'POST':
        name = request.POST['group_name']
        img = request.FILES['img']
        group = Group.objects.get(group_name=name)
        group.scrnshot = img
        group.save()
        return redirect('grouplocked', group_name=name)


@login_required(login_url='/accounts/login')
def settings(request):
    u = User.objects.get(username=request.user.username)
    if request.method == "POST":
        # Get form values
        currpw = request.POST["currpw"]
        password = request.POST["newpw"]
        user = auth.authenticate(
            request, username=request.user.username, password=currpw)
        if user is not None:
            u.set_password(password)
            u.save()
            auth.login(
                request, u, backend="django.contrib.auth.backends.ModelBackend"
            )
            messages.success(request, "Your profile was updated successfully")
            return redirect("settings")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("settings")
    else:
        return render(request, "accounts/settings.html")


@login_required(login_url='/accounts/login')
def report(request):
    return render(request, "accounts/report.html")


def forgetpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        # Check email
        if User.objects.filter(email=email).exists() == False:
            messages.error(
                request, "Email does not exist.")
            return redirect("forgetpassword")
        else:
            user = User.objects.filter(email=email)[0]
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
            }

            link = reverse('resetpw', kwargs={
                            'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Reset your Password'

            reset_url = 'http://shopbud.herokuapp.com'+link

            email = EmailMessage(
                email_subject,
                'Hi there, Please click the link below to reset your password \n'+reset_url,
                'noreply@semycolon.com',
                [email],
            )
            email.send(fail_silently=False)
            return redirect("resetpasswordsuccess")

    return render(request, "accounts/forgetpassword.html")

def resetpw(request, uidb64, token):
    context = {'uidb64':uidb64, 'token':token}
    if request.method == "POST":
        newpw = request.POST["password"]
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=user_id)
        
        try:
            validate_password(newpw)
        except:
            messages.error(request, password_validators_help_texts(password_validators=None))
            return redirect("resetpw", uidb64=uidb64, token=token)
        user.set_password(newpw)        
        user.save()
        messages.success(request, "Password reset successfully")
        return redirect("login")
        
    return render(request, "accounts/resetpw.html",context)

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
        name = request.POST.get("name").lower()
        tkg_number = request.POST.get("tkg_number")

        dlt = Deliveries.objects.filter(
            name=name, tkg_number=tkg_number, user_id=request.user.id)
        dlt.delete()

        return JsonResponse({"success": ""}, status=200)


def changePaidStatus(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        index = int(request.GET['index'])
        paid = True if request.GET['paid'] == 'true' else False
        data = Data.objects.get(group_name=group_name)
        data.paid[index] = paid
        data.save()
        return JsonResponse({"success": ""}, status=200)


def deleteItem(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.POST['name']
        index = int(request.POST['index'])

        data = Data.objects.filter(group_name=group_name)[0]
        data.users.pop(index)
        data.items.pop(index)
        data.quantity.pop(index)
        data.prices.pop(index)
        data.urls.pop(index)
        data.paid.pop(index)
        data.save()

        return JsonResponse({"success": ""}, status=200)


def leaveGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        grp = Group.objects.get(pk=group_name)
        data = Data.objects.filter(group_name=group_name)
        grp_shipping = Shipping.objects.get(pk=group_name)
        index = grp.members.index(request.user.username)
        grp.contacts.pop(index)
        grp.members.remove(request.user.username)
        grp.save()
        grp_shipping.member_count -= 1
        grp_shipping.save()

        # Deletes user's data when user leaves group
        if len(data) != 0:
            while request.user.username in data[0].users:
                index = data[0].users.index(request.user.username)
                data[0].items.pop(index)
                data[0].urls.pop(index)
                data[0].prices.pop(index)
                data[0].quantity.pop(index)
                data[0].paid.pop(index)
                data[0].users.remove(request.user.username)
            data[0].save()

        return JsonResponse({"success": ""}, status=200)


def lockGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        grp = Group.objects.get(pk=group_name)
        grp.is_locked = True
        grp.save()
        return JsonResponse({"success": ""}, status=200)


def deleteGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        grp_ship = Shipping.objects.get(pk=group_name)
        grp_ship.delete()
        grp = Group.objects.get(pk=group_name)
        grp.delete()
        return JsonResponse({"success": ""}, status=200)

def unlockGroup(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        group_name = request.GET['name']
        grp = Group.objects.get(pk=group_name)
        grp.is_locked = False
        grp.save()
        return JsonResponse({"success": ""}, status=200)


def onboardingFin(request):
    if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = UserExtension.objects.filter(user=request.user)

        if len(user) != 0:
            user[0].first_time_user = False
            user[0].save()
            return JsonResponse({"success": ""}, status=200)
