from django.shortcuts import render,redirect
from django.contrib import messages
from app.auth import authentication,input_verification,input_verification1
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from app.models import *
from django.db.models import Q
import numpy as np
import pickle
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .modify import modify_msg
# Create your views here.
def index(request):
    return render(request, "index.html", {'navbar' : 'home'})

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def chatbot(request):
    return render(request, "chatbot.html")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            # Call the modify_msg function
            response, links = modify_msg(user_message)
            links_list = links.split('\n')  # Split links into a list if needed

            return JsonResponse({
                'response': response,
                'links': links_list
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        # Validate user input
        verify = authentication(first_name, last_name, password, password1, phone_number)
        if verify == "success":
            # Prevent duplicate usernames (email)
            if User.objects.filter(username=username).exists():
                messages.error(request, "This email/username is already registered. Please log in or use another email.")
                return redirect("register")

            try:
                # Correctly create user: username and password as keyword args; use username as email
                user = User.objects.create_user(username=username, password=password, email=username)  # create_user
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            except Exception as e:
                messages.error(request, f"Could not create account: {e}")
                return redirect("register")

            # Send confirmation email
            subject = 'Account Created Successfully'
            message = f'Hello {first_name},\n\nYour account has been successfully created. Welcome to our platform!'
            from_gmail = settings.EMAIL_HOST_USER  # This will use your email from settings.py
            recipient_list = [username]  # Email the user the username they registered with
            
            # Sending the email
            send_mail(subject, message, from_gmail, recipient_list, fail_silently=False)

            # Success message
            messages.success(request, "Your account has been created and a confirmation email has been sent.")
            return redirect("log_in")
            
        else:
            messages.error(request, verify)
            return redirect("register")
    
    return render(request, "register.html", {'navbar': 'register'})


def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html", {'navbar' : 'log_in'})

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def crop_report(request):
    crop_data = Crop_Details.objects.last()
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
        'crop_data' : crop_data
    }
    if request.method == "POST":
        return redirect("report")
    return render(request, "crop_report.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def fert_report(request):
    fert_data = fert_Details.objects.last()
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
        'fert_data' : fert_data
    }
    if request.method == "POST":
        return redirect("report1")
    return render(request, "fert_report.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def report(request):
    crop_data = Crop_Details.objects.last()
    context = { 
        'crop_data' : crop_data
    }
    return render(request, "report.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def report1(request):
    fert_data = fert_Details.objects.last()
    context = { 
        'fert_data' : fert_data
    }
    return render(request, "report1.html", context)

def crop_prediction(request):
    if request.method == "POST":
        farmer_name = request.POST['farmer_name']
        contact_no = request.POST['contact_no']
        n = request.POST['n']
        p = request.POST['p']
        k = request.POST['k']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']
        
        verify = input_verification(farmer_name, contact_no, n, p, k, temperature, humidity, ph, rainfall)
        if verify == "Success":
            with open('dataset/crop_Prediction.pkl', 'rb') as f:
                NaiveBayes = pickle.load(f)
            data = np.array([[n,p,k,temperature,humidity,ph,rainfall]], dtype=float)
            pred = NaiveBayes.predict(data)

            message = 'Predicted Crop is : ' + pred[0]
            crop = Crop_Details(farmer_name = farmer_name, contact_no = contact_no, n = n, p = p, k = k, temperature = temperature, humidity= humidity, ph = ph, rainfall = rainfall)
            crop.prediction = message
            crop.date = datetime.today()
            crop.save()
            messages.info(request, message)
            return redirect("crop_report")
        else:
            messages.error(request, verify)
            return redirect("dashboard")
    return render(request, "crop_prediction.html", {'navbar': 'home'})

def fert_rec(request):
    if request.method == "POST":
        farmer_name = request.POST['farmer_name']
        n = request.POST['n']
        p = request.POST['p']
        k = request.POST['k']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        moisture = request.POST['moisture']
               
        verify = input_verification1(farmer_name, n, p, k, temperature, humidity, moisture)
        if verify == "Success":
            with open('dataset/Fertilizer_Classifier.pkl', 'rb') as f:
                NaiveBayes = pickle.load(f)
            data = np.array([[n,p,k,temperature,humidity,moisture]], dtype=float)
            pred = NaiveBayes.predict(data)
            message = 'Predicted Fertilizer is : ' + pred[0]
            fert = fert_Details(farmer_name = farmer_name, n = n, p = p, k = k, temperature = temperature, humidity= humidity, moisture = moisture, fertilizer = pred)
            fert.prediction = message
            fert.date = datetime.today()
            fert.save()
            messages.info(request, message)
            return redirect("fert_report")
        else:
            messages.error(request, verify)
            return redirect("dashboard")
    return render(request, "fert_rec.html", {'navbar': 'home'})