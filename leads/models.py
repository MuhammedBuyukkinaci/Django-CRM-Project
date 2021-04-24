from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
#User


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

    def __str__(self):
        return "{} is the username".format(self.username)

    # def __str__(self):
    #     return

    pass
    #To add something like cellphone number:
    #cellphone = models.CharField(max_length=20)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
# Create your models here.

# Creating a Lead table
class Lead(models.Model):

    # SOURCE_CHOICES = (
    #     ('Youtube','Youtube'),
    #     ('Google','Google'),
    #     ('Newsletter','Newsletter')
    # )

    first_name = models.CharField(max_length= 20)
    last_name = models.CharField(max_length= 20)
    age = models.IntegerField(default = 0)
    #models.CASCADE means deleting Lead in case Agent is deleted
    #agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    # related_name="leads" is used in get_context_data method of CategoryDetailView
    category = models.ForeignKey("Category",related_name="leads",null=True, blank=True,on_delete=models.SET_NULL)
    
    # phoned = models.BooleanField(default=False)
    # source = models.CharField(choices = SOURCE_CHOICES,max_length=100)

    # # blank & null are different
    # # We are able to save image without a profile picture.
    # profile_picture = models.ImageField(blank = True, null = True)
    # special_files = models.FileField(blank = True, null = True )

    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)


# Creating a Agent table
class Agent(models.Model):
    #Map 1 User to 1 Agent
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Category(models.Model):
    # New, Contacted, Converted, Unconverted
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

def post_user_created_signal(sender, instance, created,**kwargs):
    print(instance,created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal,sender = User)