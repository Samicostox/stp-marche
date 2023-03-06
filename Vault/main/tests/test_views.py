from django.test import TestCase, Client
from django.urls import reverse
from main.models import *
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.meal_url = reverse('meal')
        self.openai_url = reverse('openai_populate')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.reco_url = reverse('reco')
        self.onemeal_url = reverse('reco')


        self.user = User.objects.create(
            username = "toto",
            email = "sam.rib@g.com",
            password = "333333xxx",
            age = 26,

        )



    def test_project_meal_GET(self):

        
        response = self.client.get(self.meal_url)

        self.assertEquals(response.status_code,200)
    
    def test_project_detail_POST_Register(self):
        
        response = self.client.post(self.register_url,{
            'username' : self.user.username,
            'email' : self.user.email,
            'password' : self.user.password,
            'age' : self.user.age,
            'isemailvalid' : True,

        })

        self.assertEquals(response.status_code,200)
        self.assertEquals(self.user.username,"toto")

    def test_project_login_POST(self):

        response = self.client.post(self.login_url,{
            'email' : self.user.email,
            'password' : self.user.password,
            

        })

        self.assertEquals(response.status_code,200)
        self.assertEquals(self.user.username,"toto")

    
    def test_project_profile_POST(self):
        

        response = self.client.post(self.profile_url,{
            'user_id' : self.user.id
            

        })
        

        self.assertEquals(response.status_code,200)

    
    def test_project_reco_POST(self):
        

        response = self.client.post(self.reco_url,{
            'user_id' : self.user.id
            

        })
        

        self.assertEquals(response.status_code,200)
    
    def test_project_onemeal_POST(self):

        meal = Meal.objects.get(pk=2)
        

        response = self.client.post(self.onemeal_url,{
            'meal_id' : meal.id
            

        })
        

        self.assertEquals(response.status_code,200)
        
        



