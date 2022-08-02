import email
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from talk.models import NewUser
import random
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


# Redirecting to check if user is already logined
def redirectToTalk(request):
    return redirect("/talk")

def home(request):
    return render(request, "index.html")


def login(request):
    # When the page is redirected from signup:
    if request.GET:
        return render(request, "login.html", {"additionalMsg": "Signup successful, Please login to proceed:"})

    # When someone enter direct url
    else:
        return render(request, "login.html")


def signupErr(request):
    # When the email already exist that is typed for creating new account
    return render(request, "signup.html", {"additionalMsg": "Email already exist, Please try a different one."})


stringForRandom = '''abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+}|"{:>?<[];'\/.,`'}'''

# This creates random complex strings to be added as unique id
def generateRandID():
    randomId = ""
    for i in (random.choices(stringForRandom, k = 21)):
        randomId += i
    if NewUser.objects.filter(unique_id = randomId).exists():
        generateRandID()
    else:
        return randomId

# For sending otp on email for email verification
def sendOTP(request):

    plainEmail = request.POST["email"]
    # global declaredOTP
    declaredOTP = ""
    for eachNum in (random.choices("0123456789", k=6)):
        declaredOTP += eachNum

    htmly = get_template('Email.html')
    d = { 'otp':declaredOTP }
    subject, from_email, to = 'OTP for talkish web app', 'talkish.com', plainEmail
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Setting the otp hash in cookie
    resp = JsonResponse({})
    resp.set_cookie("oid", make_password(declaredOTP), 600)
    return resp

def verifyEmail(request):
    # If the request is from fronend
    if request.POST:

        enteredOTP = request.POST["enteredOTP"]
        if check_password(enteredOTP, request.COOKIES["oid"]):
            email = request.POST["email"]
            
            return JsonResponse({"err": "otp test passed and now inside"})


            # Checking if email already exist:

            # Here, if the email exist then the below query will return the len of object as "1" which is true in binary
            if len(NewUser.objects.filter(userEmail=email)):
                return JsonResponse({"location":"/signupErr"})
            
            else:
                fName = request.POST["firstName"]
                lName = request.POST["lastName"]
                plainPwd = request.POST["password"]
                hashedPwd = make_password(plainPwd)
                uniqueId =generateRandID()

                # Adding the new user in database:
                data = NewUser(firstName=fName, lastName=lName,
                            userEmail=email, userPassword=hashedPwd,
                            unique_id = uniqueId)
                data.save()
                return JsonResponse({"location":"/login?y"})

        else:
            return JsonResponse({"location":"OTPErr"})
            
    # If the url entered directly
    else:
        return redirect("/signup")



def signup(request):
    return render(request, "signup.html")
