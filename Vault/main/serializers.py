from rest_framework import serializers
from .models import Preferences, User, Physic,Meal, TestList, SignUpToken, ratings, Store
from drf_extra_fields.fields import Base64ImageField
import base64


class UserSerializer(serializers.ModelSerializer):
    image_memory=serializers.SerializerMethodField("get_image_memory2")
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','profilepic','image_memory','age']
    
    def get_image_memory2(request,user:User):
            with open("media/"+user.profilepic.name, 'rb') as loadedfile:
                return base64.b64encode(loadedfile.read())
            return  

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    


class PhysicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Physic
        fields = ['id','height','weight','goal','duration','weight_goal','user','height_timestamp','weight_timestamp']

class PreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preferences
        fields = ['id', 'fav_ingredients', 'fav_crountry_meal','budget','fav_complexity','fav_meals','user']


class MealSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description','ingredients','steps','nutri_values','foodpic','recipe_id','n_steps','tags','rating']

    def get_image_memory(request,meal:Meal):
            with open("media/"+meal.foodpic.name, 'rb') as loadedfile:
                return base64.b64encode(loadedfile.read())
            return  


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestList
        fields = ['id','ingredients']


class SignUpTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = SignUpToken
        fields = ['id', 'timestamp','user','code']

class RateMealSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model = ratings
        fields = ['id', 'user' ,'meal', 'rating']


class StoreSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model = Store
        fields = ['id', 'corr']