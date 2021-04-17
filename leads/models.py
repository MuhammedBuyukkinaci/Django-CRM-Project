from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.contrib.auth.models import AbstractUser

#User


class User(AbstractUser):
    pass
    #To add something like cellphone number:
    #cellphone = models.CharField(max_length=20)

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
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

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
    
    def __str__(self):
        return self.user.email

