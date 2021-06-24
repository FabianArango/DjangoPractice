import json, time
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils import timezone
from django.core.files import File
from django import db
from . import urls, models, consumers

# Create your views here.

def index(request):
    template = loader.get_template("home/index.html")
    return HttpResponse(template.render())

def ajaxMain(request):
    """
    print(urls.urlpatterns)

    for patter in urls.urlpatterns:
    """
    return HttpResponse(
        render(
            request, 
            "home/ajaxMain.html",
            context={
                "myList": ["ajax", "ajaxjq", "ajaxjqcsrf", "home"]
            }
        )
    )

def ajax(request):
    template = loader.get_template("home/ajax/ajax.html")
    return HttpResponse(template.render())

@csrf_exempt
def ajaxjq(request):
    return HttpResponse(render(request, "home/ajax/ajaxjq.html"))

def ajaxjqcsrf(request):
    template = loader.get_template("home/ajax/ajaxjqcsrf.html")
    return HttpResponse(template.render())

def download(request):
    template = loader.get_template("home/download.html")
    return HttpResponse(template.render())

def space(request):
    template = loader.get_template("home/space.html")
    return HttpResponse(template.render())

def response(request, letter):
    a = list()

    a.append("Anna")
    a.append("Brittany")
    a.append("Cinderella")
    a.append("Diana")
    a.append("Eva")
    a.append("Fiona")
    a.append("Gunda")
    a.append("Hege")
    a.append("Inga")
    a.append("Johanna")
    a.append("Kitty")
    a.append("Linda")
    a.append("Nina")
    a.append("Ophelia")
    a.append("Petunia")
    a.append("Amanda")
    a.append("Raquel")
    a.append("Cindy")
    a.append("Doris")
    a.append("Eve")
    a.append("Evita")
    a.append("Sunniva")
    a.append("Tove")
    a.append("Unni")
    a.append("Violet")
    a.append("Liza")
    a.append("Elizabeth")
    a.append("Ellen")
    a.append("Wenche")
    a.append("Wendy")
    a.append("Vicky")
    a.append("Monika")
    a.append("Mariana")
    a.append("Maria")
    a.append("Martha") 

    names = list()
    for name in a:
        if name[0].lower() == letter.lower():
            names.append(name)

    return HttpResponse("no suggestion" if len(names) == 0 else ", ".join(names))

@csrf_exempt
def responsePost(request):
    a = list()

    a.append("Anna")
    a.append("Brittany")
    a.append("Cinderella")
    a.append("Diana")
    a.append("Eva")
    a.append("Fiona")
    a.append("Gunda")
    a.append("Hege")
    a.append("Inga")
    a.append("Johanna")
    a.append("Kitty")
    a.append("Linda")
    a.append("Nina")
    a.append("Ophelia")
    a.append("Petunia")
    a.append("Amanda")
    a.append("Raquel")
    a.append("Cindy")
    a.append("Doris")
    a.append("Eve")
    a.append("Evita")
    a.append("Sunniva")
    a.append("Tove")
    a.append("Unni")
    a.append("Violet")
    a.append("Liza")
    a.append("Elizabeth")
    a.append("Ellen")
    a.append("Wenche")
    a.append("Wendy")
    a.append("Vicky")
    a.append("Monika")
    a.append("Mariana")
    a.append("Maria")
    a.append("Martha") 

    names = list()
    for name in a:
        if name[0].lower() == request.POST.dict()["letter"].lower():
            names.append(name)
            
    return HttpResponse("no suggestion" if len(names) == 0 else ", ".join(names))


@csrf_exempt
def signUp(request):
    return render(request, "home/accounts/signUp.html")

@csrf_exempt
def checkNewUser(request):
    post = request.POST

    username = post.get("username")
    password = post.get("password")

    if username == "":
        return HttpResponse("Ivalid blank username")
    print("username")

    if password == "":
        return HttpResponse("Ivalid blank password")
    print("password")

    if username.replace(" ", "") == "":
        return HttpResponse("usernames cannot contain spaces")
    print("username space")

    if " " in password:
        return HttpResponse("passwords cannot contain spaces")
    print("password space")

    if models.User.objects.filter(username=username).exists():
        return HttpResponse("The username already exists")
    print("username used")

    if len(password) < 8:
        return HttpResponse("The password must be at least 8 characters long")
    print("passwordlen")

    user = models.User(username=username, password=password, creationDate=timezone.now())
    user.save()
    print("username saved")

    # no puede ser == ""
    # el nombre de usuario no debe estar usado
    # la contraseña de tener mas de 8 caracteres

    # si todo esta bien, se procede a la siguiente página

    # si algo esta mal, se devuelve que esta mal
    response = HttpResponse("True")
    response.set_cookie("username", username)
    response.set_cookie("password", password)
    return response

@csrf_exempt
def accountData(request):
    print(request.COOKIES)
    if "username" in request.COOKIES and "password" in request.COOKIES:
        user = models.User.objects.filter(username=request.COOKIES["username"])
        if user.exists():
            if user.get().password == request.COOKIES["password"]:
                return render(
                    request, 
                    "home/accounts/accountData.html", 
                    context={
                        "username": request.COOKIES["username"],
                        "password": request.COOKIES["password"],
                        "creationDate": user.get().creationDate,
                        "description": user.get().description,
                        "profilePic": user.get().profilePic.url
                    }
                )

    return redirect("home:logIn")

@csrf_exempt
def changePassWord(request):
    return render(request, "home/accounts/changePassword.html")

@csrf_exempt
def validateNewPassword(request):
    post = request.POST
    oldPassword = post.get("oldPassword")
    newPassword = post.get("newPassword")
    newPasswordCon = post.get("newPasswordCon")

    if oldPassword == "" or newPassword == "" or newPasswordCon == "":
        return HttpResponse("Ivalid blank password")

    if " " in oldPassword or " " in newPassword or " " in newPasswordCon:
        return HttpResponse("passwords cannot contain spaces")

    if len(oldPassword) < 8 or len(newPassword) < 8 or len(newPasswordCon) < 8:
        return HttpResponse("The password must be at least 8 characters long")

    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        user = models.User.objects.filter(username=username)

        if user.exists():
            if user.get().password == oldPassword:
                if newPassword == newPasswordCon:
                    userpass = user.get()
                    userpass.password = newPassword
                    userpass.save()
                    response = HttpResponse("Password changed succesfully")
                    response.set_cookie("password", newPassword)
                    return response

                return HttpResponse("The new password does not match")
            
            return HttpResponse("Invalid old password")

        return HttpResponse("The user does not exists")

    return redirect("home:logIn")

@csrf_exempt
def logIn(request):
    return render(request, "home/accounts/logIn.html")

@csrf_exempt
def logInCheck(request):
    post = request.POST

    username = post.get("username")
    password = post.get("password")

    if username == "":
        return HttpResponse("Ivalid blank username")
    print("username")

    if password == "":
        return HttpResponse("Ivalid blank password")
    print("password")

    if username.replace(" ", "") == "":
        return HttpResponse("usernames cannot contain spaces")
    print("username space")

    if " " in password:
        return HttpResponse("passwords cannot contain spaces")
    print("password space")

    if len(password) < 8:
        return HttpResponse("The password must be at least 8 characters long")
    print("passwordlen")

    user = models.User.objects.filter(username=username)
    if user.exists():
        if user.get().password == password:
            response = HttpResponse("True")
            response.set_cookie("username", username)
            response.set_cookie("password", password)
            return response

        else:
            return HttpResponse("Incorrect Password")

    else:
        return HttpResponse("The username does not exists")

def logOutCheck(request):
    response = HttpResponse("Log Out Succesfuly")
    response.delete_cookie("username")
    response.delete_cookie("password")
    return response


def deleteUser(request):
    response = redirect("home:home")
    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]

        user = models.User.objects.filter(username=username)
        if user.exists() and user.get().password == password:
            user.delete()
            response.delete_cookie("username")
            response.delete_cookie("password")

    return response

@csrf_exempt
def csrfAttack(request):
    return render(request, "home/attac/csrf.html")

@csrf_exempt
def profilePic(request):
    return render(request, "home/accounts/profilePic.html")

@csrf_exempt
def addProfilePic(request):
    print(request.FILES)    
    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]
        user = models.User.objects.filter(username=username)

        if user.exists():
            profilePic = request.FILES["profilePic"]
            path = "static/upload/profilePic/"
            file_name = f"{username}"+profilePic.name[-4:]

            if default_storage.exists(path+file_name):
                default_storage.delete(path+file_name)

            #file = default_storage.save(path+file_name, profilePic)

            userPic = user.get()
            #userPic.profilePic = db.models.FileField(upload_to=f"static/upload/profilePic/"+file_name, default="static/upload/profilePic/default.gif")
            userPic.profilePic.save(file_name, profilePic)
            userPic.save()
        
    return HttpResponse("profile pic changed succesfully!")


@csrf_exempt
def changeUserDescription(request):
    print(request.POST)

    description = request.POST.get("description")

    if len(description) > 254:
        return HttpResponse("The description is very large")

    if description == "" or description.replace(" ", "") == "":
        return HttpResponse("Empty descriptions are not valid")

    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]
        user = models.User.objects.filter(username=username)
        if user.exists():
            userDes = user.get()
            userDes.description = request.POST.get("description")
            userDes.save()

    return HttpResponse("Description changed successfuly") 

def getDescription(request):
    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]
        user = models.User.objects.filter(username=username)

        if user.exists():
            userDes = user.get()
            return HttpResponse(userDes.description)

    return HttpResponse("None")

@csrf_exempt
def postContent(request):
    return render(request, "home/post/postContent.html")

@csrf_exempt
def newPost(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content == "" or content.replace(" ", "") == "":
            return HttpResponse("Empy content are not valid")

        if len(content) > 254:
            return HttpResponse("The content is very large")

        if "username" in request.COOKIES and "password" in request.COOKIES:
            username = request.COOKIES["username"]
            password = request.COOKIES["password"]
            user = models.User.objects.filter(username=username)
            if user.exists():
                userDes = user.get()
                if userDes.password == password:
                    userPost = models.UserPost(username=username, content=content, creationDate=timezone.now())
                    userPost.save()
                    print("before True")

                    print("after True")
                    return HttpResponse("Content posted successfully")
                
                return HttpResponse("Invalid password")
            
            return HttpResponse("The user name does not exists")

        return HttpResponse("Error: No user name logged")

    return HttpResponse("Bad request")

@csrf_exempt
def allPosts(request):
    return render(request, "home/post/allThePosts.html")

def getAllUserPosts(request):
    allPosts = models.UserPost.objects.all()
    postList = dict()
    #i = len(models.UserPost.objects.all())-1
    i = 0
    for post in allPosts:
        postList[i] = {
            "username": post.username,
            "content": post.content,
            "creationDate": post.creationDate
        }
        i += 1

    #postList = dict(sorted(postList.items())) 
    #print(postList)
    return JsonResponse(postList)

"""
def getLastPost(request):
    global new

    while True:
        time.sleep(1)
        if new:
            new = False
            break

    last = models.UserPost.objects.latest("creationDate")
    return JsonResponse(
        {
            "username": last.username,
            "content": last.content,
            "creationDate": last.creationDate
        }
    )
"""

@csrf_exempt
def getLastPost(request):
    index = request.POST.get("index")
    index = int(index)

    print(index)
    print(len(models.UserPost.objects.all())-1)

    new = "false"
    username = "None"
    content = "None"
    creationDate = "None"

    if len(models.UserPost.objects.all())-1 > index: 
        last = models.UserPost.objects.all()[index+1]
        new = "true"
        username = last.username
        content = last.content
        creationDate = last.creationDate

    return JsonResponse(
        {
            "new": new,
            "data": {
                "username": username,
                "content": content,
                "creationDate": creationDate
            }
        }
    )

def chatAll(request):
    return render(request, "home/chat/index.html")

def room(request, room_name):
    return render(request, 'home/chat/room.html', {
        'room_name': room_name
    })

@csrf_exempt
def sendFriendRequest(request):
    if "username" in request.COOKIES and "password" in request.COOKIES:
        logUsername = request.COOKIES["username"]
        user = models.User.objects.filter(username=logUsername)
        if user.exists():
            if user.get().password == request.COOKIES["password"]:
                return render(request, "home/friends/sendFriendRequest.html")

    return redirect("home:logIn")

@csrf_exempt
def getUserList(request):
    if "username" in request.COOKIES and "password" in request.COOKIES:
        logUsername = request.COOKIES["username"]
        user = models.User.objects.filter(username=logUsername)
        if user.exists():
            if user.get().password == request.COOKIES["password"]:
                if request.method == "POST":
                    username = request.POST.get("username")

                    if username == "" or username.replace(" ", "") == "":
                        username = " "
                    
                    userList = models.User.objects.filter(username__regex=username).values_list("username", "profilePic")
                    userList = list(userList)

                    if (logUsername, user.get().profilePic) in userList:
                        userList.remove((logUsername, user.get().profilePic))

                    return JsonResponse(
                        {
                            "userList": userList
                        }
                    )

@csrf_exempt
def friendRequest(request):
    if "username" in request.COOKIES and "password" in request.COOKIES:
        fromUser = request.COOKIES["username"]
        user = models.User.objects.filter(username=fromUser)
        if user.exists():
            if user.get().password == request.COOKIES["password"]:
                if request.method == "POST":
                    toUser = request.POST.get("username")

                    return HttpResponse( models.FriendRequest.sendFriendRequest(fromUser, toUser))

    return HttpResponse("Fatal error ocurr.")

@csrf_exempt
def checkFriendRequest(request):
    return render(request, "home/friends/checkFriendRequest.html")

@csrf_exempt
def acceptFriendRequest(request):
    if request.method == "POST":
        if "username" in request.COOKIES and "password" in request.COOKIES:
            username = request.COOKIES["username"]
            password = request.COOKIES["password"]

            user = models.User.objects.filter(username=username)
            if user.exists():
                if user.get().password == password:
                    acceptedUser = user.get().friendRequest.filter(username=request.POST.get("username"))
                    friendCheck = user.get().friends.filter(username=request.POST.get("username"))
                    if acceptedUser.exists():
                        a = False
                        if request.POST.get("accepted") == "true" and not friendCheck.exists():
                            u = user.get()
                            newFriend = models.UserFriends(username=acceptedUser.get().username, creationDate=timezone.now())
                            newFriend.save()
                            u.friends.add(newFriend)
                            u.save()
                            
                            u2 = models.User.objects.filter(username=request.POST.get("username")).get()
                            newFriend2 = models.UserFriends(username=username, creationDate=timezone.now())
                            newFriend2.save()
                            u2.friends.add(newFriend2)
                            u2.save()

                            a = True
                            print("accepted")
                        acceptedUser.delete()
                        if a:
                            return HttpResponse("User accepted successfully")
                        return HttpResponse("User denied successfully")

                    return HttpResponse("The user does have sended a frien request yet")
    return HttpResponse("Fatal error occ.001")

def getFriendRequest(request):
    print(request.COOKIES)
    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]

        user = models.User.objects.filter(username=username)
        if user.exists():
            if user.get().password == password:
                if request.method == "GET":
                    usernameList = list(user.get().friendRequest.values_list("username", flat=True))
                    userList = list(models.User.objects.filter(username__in=usernameList).values_list("username", "profilePic"))
                    return JsonResponse(
                        {
                            "data": userList
                        }
                    )
                return HttpResponse("Fatal error occ.004")
            return HttpResponse("Fatal error occ.003")
        return HttpResponse("Fatal error occ.002")
    return HttpResponse("Fatal error occ.001")

@csrf_exempt
def allMyFriends(request):
    return render(request, "home/friends/allMyFriends.html")

def getFriends(request):
    print(request.COOKIES)
    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]

        user = models.User.objects.filter(username=username)
        if user.exists():
            if user.get().password == password:
                if request.method == "GET":
                    usernameList = list(user.get().friends.values_list("username", flat=True))
                    userList = list(models.User.objects.filter(username__in=usernameList).values_list("username", "profilePic"))
                    return JsonResponse(
                        {
                            "data": userList
                        }
                    )
                return HttpResponse("Fatal error occ.004")
            return HttpResponse("Fatal error occ.003")
        return HttpResponse("Fatal error occ.002")
    return HttpResponse("Fatal error occ.001")

@csrf_exempt
def removeFriend(request):
    if request.method == "POST":
        if "username" in request.COOKIES and "password" in request.COOKIES:
            username = request.COOKIES["username"]
            password = request.COOKIES["password"]

            user = models.User.objects.filter(username=username)
            if user.exists():
                if user.get().password == password:
                    removedFriend1 = user.get().friends.filter(username=request.POST.get("username"))
                    removedFriend1.delete()
                    removedFriend2 = models.User.objects.filter(username=request.POST.get("username")).get().friends.filter(username=username)
                    removedFriend2.delete()
                    return HttpResponse("Friend removed successfully")
                                 
    return HttpResponse("Fatal error occ.001")


def firendProfile(request, username):
    if "username" in request.COOKIES and "password" in request.COOKIES:
        user = models.User.objects.filter(username=request.COOKIES["username"], password=request.COOKIES["password"])
        userFriend = models.User.objects.filter(username=username)
        if user.exists() and userFriend.exists():
            user = user.get()
            userFriend = userFriend.get()
            if user.friends.filter(username=username).exists():
                return render(
                    request,
                    "home/friends/seeProfile.html",
                    context={
                        "username": username,
                        "profilePic": userFriend.profilePic.url,
                        "description": userFriend.description,
                        "creationDate": userFriend.creationDate
                    }
                )

        raise Http404("Invalid user data")
    return redirect("home:logIn")

def chat(request, chatId):
    if "FriendToFriend" in chatId or chatId == "" or chatId.replace(" ", "") == "":
        raise Http404("Invalid chat name")

    return userChat(request, chatId)

def chatFriendToFriend(request, username1, username2):
    if username1 == username2:
        raise Http404("Invalid duplicate user")

    if not (request.COOKIES["username"] == username1 or request.COOKIES["username"] == username2):
        return redirect("home:logIn")

    user1 = models.User.objects.filter(username=username1)
    user2 = models.User.objects.filter(username=username2)

    if user1.exists() and user2.exists():
        if user1.get().friends.filter(username=user2.get().username):
            users = [username1, username2]
            users.sort()
            chatId = "FriendToFriend".join(users)
            print(chatId)

            return userChat(request, chatId)
        raise Http404("This users are not friends")
    raise Http404("One fo the users does not exists")

def userChat(request, chatId):
    if "username" in request.COOKIES and "password" in request.COOKIES:
        user = models.User.objects.filter(username=request.COOKIES["username"])
        if user.exists():
            if user.get().password == request.COOKIES["password"]:
                chat = models.Chat.objects.filter(chatId=chatId)
                if not chat.exists():
                    print("The chat does not exist")
                    chat = models.Chat(chatId=chatId, creationDate=timezone.now())
                    chat.save()
                    print(f"chat {chat.chatId} created successfully")
                return render(
                    request, 
                    "home/chat/globalChat.html",
                    context={
                        "chatId": chatId,
                    }
                )
    return redirect("home:logIn")

def initChat(request, chatId):
    chat = models.Chat.objects.filter(chatId=chatId).get()
    messages = list()
    for message in chat.messages.all():
        messages.append(
            consumers.UserChat.buildMessajeJSON(message.user.get().username, message.user.get().profilePic.url, message.content)
        )
    return JsonResponse(
        {
            'type': 'chat_message',
            "data": messages
        }
    )