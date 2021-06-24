from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.index, name='home'),
    
    #ajax
    path("ajax", views.ajaxMain, name="ajaxMain"),
    path("ajax/ajax", views.ajax, name="ajax"),
    path("ajax/ajaxjq", views.ajaxjq, name="ajaxjq"),
    path("ajax/ajaxjqcsrf", views.ajaxjqcsrf, name="ajaxjqcsrf"),
    path("response/<str:letter>", views.response, name="response"),
    path("post/response", views.responsePost, name="responsePost"),

    #misc
    path("space", views.space, name="space"),
    path("download", views.download, name="download"),

    #login
    path("accounts/signUp", views.signUp, name="signUp"),
    path("check/checkNewUser", views.checkNewUser, name="checkNewUser"),

    path("accounts/logIn", views.logIn, name="logIn"),
    path("check/logInCheck", views.logInCheck, name="logInCheck"),

    path("accounts/data", views.accountData, name="accountData"),

    path("check/checkLogOut", views.logOutCheck, name="logOutCheck"),

    path("accounts/changePassword", views.changePassWord, name="changePassWord"),
    path("check/passWord", views.validateNewPassword, name="validateNewPassword"),

    path("accounts/profilePic", views.profilePic, name="profilePic"),
    path("check/addProfilePic", views.addProfilePic, name="addProfilePic"),

    path("check/changeUserDescription", views.changeUserDescription, name="changeUserDescription"),
    path("check/delete", views.deleteUser, name="deleteUser"),
    #path("check/getDescription", views.getDescription, name="getDescription"),


    #post
    path("post/postContent", views.postContent, name="postContent"),
    path("check/newPost", views.newPost, name="newPost"),

    path("post/All/", views.allPosts, name="allPosts"),
    path("post/getAll", views.getAllUserPosts, name="getAllUserPosts"),
    path("post/getLast", views.getLastPost, name="getLastPost"),

    #chat
    path("chat", views.chatAll, name="chatAll"),
    path("chat/<str:room_name>/", views.room, name="room"),

    #attack
    path("attack/csrf", views.csrfAttack, name="csrfAttack"),

    path("friends/sendFriendRequest", views.sendFriendRequest, name="sendFriendRequest"),
    path("friends/getUserList", views.getUserList, name="getUserList"),
    path("friends/friendRequest", views.friendRequest, name="friendRequest"),
    path("friends/checkFriendRequest", views.checkFriendRequest, name="checkFriendRequest"),
    path("friends/getFriendRequest", views.getFriendRequest, name="getFriendRequest"),
    path("friends/acceptFriendRequest", views.acceptFriendRequest, name="acceptFriendRequest"),
    path("friends/allMyFriends", views.allMyFriends, name="allMyFriends"),
    path("friends/getFriends", views.getFriends, name="getFriends"),
    path("friends/removeFriend", views.removeFriend, name="removeFriend"),
    path("friends/firendProfile/<str:username>", views.firendProfile, name="firendProfile"),

    #chat
    path("userChat/<str:chatId>", views.chat, name="chat"),
    path("userChat/<str:username1>/<str:username2>", views.chatFriendToFriend, name="chatFriendToFriend"),
    path("initChat/<str:chatId>", views.initChat, name="initChat"),
]