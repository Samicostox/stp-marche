import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_resized import ResizedImageField
from django.contrib.postgres.fields import ArrayField



def user_directory_path(instance, filename):
    return 'images/{filename}'.format(filename=filename)


   

class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255,unique= True)
    password = models.CharField(max_length=255)
    profilepic =  ResizedImageField(size=[300, 300],
        null=True,upload_to=user_directory_path,blank=True, default='images/Lasagna.jpg'
    )
    recomeal = ArrayField(models.CharField(max_length=1000000), blank=True,default=[])
    isemailvalid = models.BooleanField(default = False)
    isnexuser = models.BooleanField(default = False)
    age = models.IntegerField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class SignUpToken(models.Model) :
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    



class Meal(models.Model):
    name = models.CharField(max_length=255)
    recipe_id = models.IntegerField()
    rating = models.IntegerField(default=0)
    nutri_values = ArrayField(models.DecimalField(max_digits=20,decimal_places=2), blank=True) # calories , fat, sugar etc
    foodpic =  models.CharField(max_length=1000)
    ingredients = ArrayField(models.CharField(max_length=2000), blank=True)
    #country = models.CharField(max_length=255)
    #complexity = models.IntegerField() # 0 easy , 1 medium, 2 hard
    description = models.CharField(max_length=5000) # description of the meal
    
    steps = ArrayField(models.CharField(max_length=5000), blank=True)
    n_steps = models.IntegerField(default=0)# implement that as an array field later
    #time = models.IntegerField(default=0) 
    tags = ArrayField(models.CharField(max_length=2000), blank=True)
    
    

class ratings (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE,related_name='m')
    rating = models.IntegerField(default=0)




class Preferences(models.Model):
    fav_ingredients = models.CharField(max_length=255) # implement that as an array field later
    fav_crountry_meal = models.CharField(max_length=255)
    budget = models.IntegerField()
    fav_complexity = models.IntegerField() # 0 easy , 1 medium, 2 hard
    fav_meals = models.CharField(max_length=255) # implement that as an array field later
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    #One to One relation to User
    
class Physic(models.Model):
    height = ArrayField(models.IntegerField(blank=True),default=list) # calories , fat, sugar etc
    weight = ArrayField(models.IntegerField(blank=True),default=list) # calories , fat, sugar etc
    height_timestamp = ArrayField(models.DateField(blank=True,),default=list)
    weight_timestamp = ArrayField(models.DateField(blank=True,),default=list)
    weight_goal = models.IntegerField(default=0)
    goal = models.IntegerField(default=2) # 1 = losing weight , 2 = maintaining weight, 3 = gaining weight
    duration = models.IntegerField(default=30)
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class TestList(models.Model):
    ingredients = ArrayField(models.CharField(max_length=200), blank=True)

class Store(models.Model):
    name = models.CharField(max_length=255)


class workout(models.Model):
    workout_list = ArrayField(ArrayField(models.CharField(max_length=5000), blank=True,default=list),blank=True,default=list)
    workout_names = ArrayField(models.CharField(max_length=5000), blank=True,default=list)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)


    def set_workout_list(self, workout_list):
        max_length = max(len(lst) for lst in workout_list)
        padded_workout_list = [lst + [None] * (max_length - len(lst)) for lst in workout_list]
        self.workout_list = padded_workout_list

    def get_workout_list(self):
        return self.workout_list