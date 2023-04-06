from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password, make_password
import re

def signup(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone_number = request.POST.get("number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        rpassword = request.POST.get("rpassword")
        description = request.POST.get("description")
        if __validate_email(email):
            if __validate_phone_number(phone_number):
                if __validate_password(password, rpassword):
                    try: 
                        user = User(name=name, phone_number=phone_number, email_id=email, password=make_password(password), description=description, active=True, is_admin=False)
                        user.save()
                        return render(request, "dashboard_app/login.html", {})
                    except IntegrityError as e:
                        messages.error(request, 'Email already exists')
                else:
                    messages.error(request, 'Password does not match')
            else:
                messages.error(request, 'Phone number is incorrect')
        else:
            messages.error(request, 'Invalid Email')
    return render(request, "dashboard_app/signup.html", {})


def login_user(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email_id=request.POST.get('email'))
            if user and check_password(request.POST.get('password'), user.password):
                request.session['id'] = user.id
                return redirect('dashboard_app:fetch_users')
            else:
                messages.error(request, 'Invalid Credentials')
        except Exception as e:
            print(e)
            messages.error(request, "Error occured, try again")
    
    return render(request, 'dashboard_app/login.html', {})


def get_all_users(request):
    if request.method == 'GET':
        id = request.session.get('id', None)
        if not id:
            return redirect('dashboard_app:login')
        logged_in_user = User.objects.get(id=id)
        if logged_in_user and logged_in_user.is_admin:
            users = User.objects.all()
        else:
            users = [logged_in_user]
        result = [{
            'id': user.id,
            'name': user.name,
            'email_id': user.email_id,
            'phone_number': user.phone_number,
            'description': user.description,
            'active': user.active
            } for user in users]
        return render(request, 'dashboard_app/users_list.html', {'object_list': result})


def update(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        is_self_user = True if request.session.get('id') == id else False
        result = {
            'id': user.id,
            'name': user.name,
            'email_id': user.email_id,
            'phone_number': user.phone_number,
            'description': user.description,
            'active': user.active
        }
        return render(request, 'dashboard_app/update_user.html', {'user': result, 'is_self_user': is_self_user})
    
    if request.method == 'POST':
        name = request.POST.get("name")
        phone_number = request.POST.get("number")
        email = request.POST.get("email")
        description = request.POST.get("description")
        active = request.POST.get("active", None)
        user = User.objects.get(id=id)
        if name:
            user.name = name
        if phone_number and __validate_phone_number(phone_number): 
            user.phone_number = phone_number
        if email and __validate_email(email):
            user.email_id = email
        if description:
            user.description = description
        if active:
            user.active = True
        else:
            user.active = False

        user.save()
        return redirect('dashboard_app:fetch_users')
       
def reset_password(request, id):
    if request.method == 'GET':
        return render(request, "dashboard_app/reset_password.html", {'id':id})

    if request.method == 'POST':
        try:
            user = User.objects.get(id=id)
            if user and check_password(request.POST.get('old_password'), user.password):
                new_password1 = request.POST.get("new_password1")
                new_password2 = request.POST.get("new_password2")
                if new_password1 == new_password2:
                    user.password = make_password(new_password1)
                    user.save()
                    result = [{
                    'id': user.id,
                    'name': user.name,
                    'email_id': user.email_id,
                    'phone_number': user.phone_number,
                    'description': user.description,
                    'active': user.active
                    }]
                else:
                    messages.error(request, "password does not match")
                    return render(request, "dashboard_app/reset_password.html", {'id':id})
            else:
                messages.error(request, "Wrond old password")
                return render(request, "dashboard_app/reset_password.html", {'id':id})
        except:
            messages.error(request, "")
        return render(request, "dashboard_app/users_list.html", {'object_list': result})


def __validate_password(password, rpassword):
    if password == rpassword:
        return True 
    return False

def __validate_phone_number(phone_number):
    if len(phone_number) == 10 and phone_number.isnumeric():
        return True
    return False

def __validate_email(email):
    return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email)
