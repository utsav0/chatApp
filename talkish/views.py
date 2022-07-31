from enum import unique
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from talk.models import NewUser
import random
from django.contrib.auth.hashers import make_password


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

def signup(request):
    if request.POST:

        # Checking if email already exist:
        email = request.POST.get("email")

        # Here, if the email exist then the below query will return the len of object as "1" which is true in binary
        if len(NewUser.objects.filter(userEmail=email)):
            return redirect("/signupErr")

        else:
            fName = request.POST.get("fName")
            lName = request.POST.get("lName")
            password = request.POST.get("password")
            hashedPassword = make_password(password)
            uniqueId = generateRandID()

            # Adding the new user in database:
            data = NewUser(firstName=fName, lastName=lName,
                           userEmail=email, userPassword=hashedPassword,
                           unique_id = uniqueId)
            data.save()

            # Extra y in the url to make it a get request so that it load login page with a success message
            return redirect("/login?y")
    else:
        return render(request, "signup.html")
