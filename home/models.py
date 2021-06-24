from django.db import models
from django.utils import timezone

# Create your models here.

def dAllUsers():
    for user in User.objects.all():
        user.delete()

def dAllPosts():
    for user in UserPost.objects.all():
        user.delete()

def dAllFriends():
    for user in UserFriends.objects.all():
        user.delete()

def dAllRF():
    for user in FriendRequest.objects.all():
        user.delete()

def dAllChat():
    for user in Chat.objects.all():
        user.delete()

def dAllMessage():
    for user in Message.objects.all():
        user.delete()


class User(models.Model):
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    creationDate = models.DateTimeField()
    profilePic = models.FileField(upload_to="static/upload/profilePic/", default="static/upload/profilePic/default.jpg")
    description = models.CharField(max_length=254, default="There is no description here")
    friends = models.ManyToManyField("UserFriends")
    friendRequest = models.ManyToManyField("FriendRequest")    

    def delete(self):
        for friend in self.friends:
            friend.delete()

        for friendRequest in self.friendRequest:
            friendRequest.delete()
        super().delete()

    def __str__(self):
        #return f"username: {self.username}, password: {self.password}, creationDate: {self.creationDate}, description: {self.description}, profilePic: {self.profilePic.url}"
        return f"""
(
    username: {self.username}, 
    password: {self.password}, 
    creationDate: {self.creationDate}, 
    description: {self.description}, 
    profilePic: {self.profilePic.url},
    friends: {self.friends.all().values_list("username", flat=True)}
    friendRequest: {self.friendRequest.all().values_list("username", flat=True)}
)
""".replace("(", "{").replace(")", "}")


class UserFriends(models.Model):
    username = models.CharField(max_length=254)
    creationDate = models.DateTimeField()

    def __str__(self):
        return f"username: {self.username}, creationDate: {self.creationDate}"


class FriendRequest(models.Model):
    username = models.CharField(max_length=254)
    creationDate = models.DateTimeField()

    def __str__(self):
        return f"username: {self.username}, creationDate: {self.creationDate}"

    @staticmethod
    def sendFriendRequest(fromUser, toUser):
        friendCheck = User.objects.filter(username=toUser).get().friends.filter(username=fromUser)
        if friendCheck.exists():
            return "This user is already your friend"
        userTo = User.objects.filter(username=toUser)
        if userTo.exists():
            if not User.objects.filter(username=toUser).get().friendRequest.filter(username=fromUser).exists():
                userDes = userTo.get()
                friendRequest = FriendRequest(username=fromUser, creationDate=timezone.now())
                friendRequest.save()

                userDes.friendRequest.add(friendRequest)
                userDes.save()

            return "Friend request sended successfully"

        return "Username does not exists"


class UserPost(models.Model):
    username = models.CharField(max_length=254)
    content = models.CharField(max_length=254)
    creationDate = models.DateTimeField()

    def __str__(self):
        return f"""
(
    username: {self.username}, 
    content: {self.content}, 
    creationDate: {self.creationDate}
)
""".replace("(", "{").replace(")", "}")

class Chat(models.Model):
    chatId = models.CharField(max_length=508)
    messages = models.ManyToManyField("Message")
    creationDate = models.DateTimeField()

    def __str__(self):
        return f"chatId: {self.chatId}, messages: {self.messages.all()}"


class Message(models.Model):
    user = models.ManyToManyField("User")
    content = models.CharField(max_length=254)
    creationDate = models.DateTimeField()

    def __str__(self):
        return f"user: {self.user}, creationDate: {self.creationDate}, content: {self.content}"

