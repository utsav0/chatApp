from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from talk.models import NewUser, Message
from django.contrib.auth.hashers import check_password
from datetime import datetime

# Create your views here.

# This connects the view of root and this app
def loginErr(request):
    email = request.POST.get("email")
    plainPassword = request.POST.get("password")

    # When credentials match:

    # When email exist
    if len(NewUser.objects.filter(userEmail=email)):

        # When password matches with the password of given email
        if check_password(plainPassword ,NewUser.objects.filter(userEmail=email)[0].userPassword):
            unique_id = (NewUser.objects.values("unique_id").get(userEmail=email)["unique_id"])

            curUserID = (NewUser.objects.values("id").get(userEmail=email)["id"])

            response = redirect("/talk")
            response.set_cookie('unique_id', unique_id, 2592000)
            response.set_cookie('curUserID', curUserID, 2592000)
            return response

        # When Email exist but password does not match
        else:
            return render(request, "login.html", {"additionalMsg": "Credentials did not match, Please try again:"})

    # When email does not exists:
    else:
        return render(request, "login.html", {"additionalMsg": "Credentials did not match, Please try again:"})


def everyone(request):
    try:
        global uniqueId
        curUserID = request.COOKIES['curUserID']
        uniqueId = request.COOKIES['unique_id']

        # If the cookies found matches with db
        if  str(NewUser.objects.values("id").get(unique_id = uniqueId)["id"])== curUserID:
            pass

        # Else create an error to run "except" to redirect
        else:
            Intentional_Error

    except:
        return redirect("/home")
        
    userLst = NewUser.objects.values_list("firstName", "lastName", "id")
    curUserDetail = NewUser.objects.filter(id=curUserID)
    return render(request, "talk/everyone.html", {"userLst": userLst, "curUserID": int(curUserID), "curUserDetail": curUserDetail})


def search(request):

    # When request is from nav bar
    if request.POST:
        query = request.POST.get("q")
        rawQuery = query
        exactMatchLst = []
        partialMatchLst = []

        # When query is not empty
        if query != "":

            # When query has Whitespace(s)
            if " " in query:
                query = query.split(" ")
                hasSpace = True

            # When query don't have Whitespace(s)
            else:
                query = [query]
                hasSpace = False

            # Checking if the name matches exactly
            if hasSpace == True and len(query) == 2:
                if NewUser.objects.filter(firstName=query[0], lastName=query[1]).exists:

                    exactMatch = NewUser.objects.filter(
                        firstName=query[0], lastName=query[1])
                    exactMatchLst.append(exactMatch)

            # *If atleast one exact name matches
            if len(exactMatchLst) > 0:
                # pass the matcheduserlist to the frontend and skip the rest of the function
                return render(request, "talk/search.html", {"exactMatchLst": exactMatchLst[0], "rawQuery": rawQuery, "exactMatchContent": "found"})

            # If not matched exactly, then search for partial matches
            else:

                # Getting the list of all users name
                AllUserLst = NewUser.objects.values(
                    "firstName", "lastName", "id")

                # Checking if the query matches
                for user in AllUserLst:
                    for name in query:
                        if name == user["firstName"] or name == user["lastName"]:
                            partialMatchLst.append(user)

                # Mentioning if related matches found or not
                if len(partialMatchLst) == 0:
                    extraMsg = "Neither any exact matches found nor any related"
                else:
                    extraMsg = "No exact matches found but here are related ones:"

                return render(request, "talk/search.html", {"partialMatchLst": partialMatchLst, "rawQuery": rawQuery, "exactMatchContent": "not found", "extraMsg": extraMsg})

        # When query is empty
        else:
            return redirect("/talk")

    # When the url is entered directly
    else:
        return redirect("/")


def addMsgToDB(request):

    if request.POST:

        # Getting data from cookies
        firstSender = request.COOKIES["firstSender"]
        curCombo = request.COOKIES["curCombo"]
        curComboAlternate = request.COOKIES["curComboAlternate"]

        msg = request.POST["msgTxt"]
        dnt = datetime.now

        # Setting it to use when the cookie is not needed to be reset
        response = JsonResponse({})

        # Save message with the normal combination
        if firstSender == "me":
            newMsg = Message(combo=curCombo, sender="me", message=msg)

        # Save message with alternae combo
        elif Message.objects.filter(combo=curComboAlternate).exists():
            newMsg = Message(combo=curComboAlternate,
                             sender="other", message=msg)

        # Create a new database with current combo
        else:
            newMsg = Message(combo=curCombo, sender="me", message=msg)
            firstSender = "me"

            response = JsonResponse({})
            response.set_cookie("firstSender", firstSender)  # Cookie reset

        newMsg.save()
        return response
    else:
        return redirect("login")


def chat(request):

    if request.POST:
        # Getting user ID of the logined user:
        curUserID = request.COOKIES['curUserID']

        # Getting the user ID of the user clicked
        toChatUserID = request.POST.get("userID")

        # Combination of person itself and the person to talk
        curCombo = f"{curUserID}&{toChatUserID}"

        # Declaring this to use in case if the logined user is not the one on who's name the message combination is created in database
        curComboAlternate = f"{toChatUserID}&{curUserID}"

        # If messages exist in normal combination for "combo"
        if Message.objects.filter(combo=curCombo).exists():
            firstSender = "me"
            curComboMsg = Message.objects.filter(combo=curCombo)

        # If messages exist with opposite combination for "combo"
        else:
            firstSender = "other"
            curComboMsg = Message.objects.filter(combo=curComboAlternate)

        # Getting the name of the person to whom message has to be sent to show on the top of the chat
        userName = NewUser.objects.filter(id=toChatUserID)[0]
        userName = userName.firstName + " " + userName.lastName

        # This is to add save data in cookies
        resp = render(request, "talk/chat.html", {"curComboMsg": curComboMsg,
                      "firstSender": firstSender, "userName": userName, "toChatUserID": toChatUserID})
        resp.set_cookie('firstSender', firstSender)
        resp.set_cookie('curCombo', curCombo)
        resp.set_cookie('curComboAlternate', curComboAlternate)

        return resp

    else:
        # If someone tries to access this page via direct url
        return redirect("login")

# For checking if the new message added to database


def checkNewMsg(request):

    # Getting saved variables from cookies
    firstSender = request.COOKIES["firstSender"]
    curCombo = request.COOKIES["curCombo"]
    curComboAlternate = request.COOKIES["curComboAlternate"]

    # Getting the last message between these two users
    if firstSender == 'me':
        newMsg = Message.objects.filter(
            combo=curCombo, sender="other").values().last()
    else:
        newMsg = Message.objects.filter(
            combo=curComboAlternate, sender="me").values().last()

    # When there's no message in the database with any of the two combinations
    if newMsg == None:
        return JsonResponse({"msg": None})

    # When there's one or more message in the database with any of the two combinations
    else:
        newMsg = newMsg["message"]
        return JsonResponse({"msg": newMsg})

# For logout
def logout(request):
    response = redirect("/")
    response.delete_cookie("curUserID")
    response.delete_cookie("unique_id")
    return response



