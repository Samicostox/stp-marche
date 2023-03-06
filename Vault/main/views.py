from datetime import date, timezone
import datetime
from heapq import merge
from django.shortcuts import render
import openai
import pandas as pd
import psycopg2
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import time


from main.thread import testThread
from .serializers import RateMealSerializer, UserSerializer, PhysicSerializer, PreferencesSerializer,MealSerializer, TestSerializer, SignUpTokenSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Physic, Preferences, Meal, TestList, SignUpToken, ratings,workout
from rest_framework.parsers import MultiPartParser, FormParser
from django.urls import reverse
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
import random
from .utils import Util
from django.core.exceptions import ObjectDoesNotExist
import json
import numpy as np
from django.db.models import Case, When
from django.http import HttpResponse
from asgiref.sync import sync_to_async
from django.db.models import F
from django.db.models import Q


class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            user_data = serializer.data
            user=User.objects.get(email=user_data['email'])
            token=RefreshToken.for_user(user).access_token

            current_site=get_current_site(request).domain

            relativeLink = reverse('email_verify')

            randomnumber = random.randrange(100000, 999999)
            absurl='http://'+current_site+relativeLink+"?token="+str(token)
            email_body='Dear ' + user.username + ',\n' 'Please use the number below in the application to verify your account \n' + str(randomnumber)
            data={'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify your email '}
            Util.send_email(data)

            workout_profile = workout.objects.create(user=user)
            workout_profile.save()
            
            s = SignUpTokenSerializer(data = {
                'user' : user.id,
                'code' : randomnumber
                })
            if s.is_valid() :
               s.save()
                

            p = Physic.objects.create(user = user)
            p.save()
            return Response(
                {
                    'msg' : 'success',
                    'code' : randomnumber,
                    'id' : user.id,
                    'msg3' : s.data,
                    
                    
                }
            )
        return Response(
                {
                    'msg' : 'Username or email are already used'  
                }
            )


class EmailPageView(APIView):
    def post(self,request):
        user_id = request.data['userid']
        user_code = request.data['code']
        user = User.objects.filter(pk=user_id).first()
       
        usertoken = SignUpToken.objects.filter(user=user_id).first()
        if (int(user_code) == usertoken.code):
            user.isemailvalid = True
            user.save()
            usertoken.delete()
            return Response({
                'msg' : 'Email Verified Successfully',
            })

        return Response ({
            'msg' : 'Wrong code'
        })




# user = User.objects.get(pk=serializer.data['id'])
           # p = Physic(user=user)
           # p.save()
class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass




class LoginView(APIView):
     def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        
        s = UserSerializer(user)


        if user is None:
            return Response({
            'msg' : 'User not found !',
            'detail': 0,
            'name' : 'NA',
            'image' : 'NANA',
        })

        if not user.check_password(password):
            return Response({
            'msg' : 'Incorrect password !',
            'detail': 0,
            'name' : 'NA',
            'image' : 'NANA',
        })

        if (user.isnexuser == False):
             return Response({
            'msg' : 'go to rating',
            'detail': user.id,
            'name' : user.username,
            'image' : s.data['image_memory'],
        })


        
        
        

        response = Response()

        
        response.data = {
                'detail': user.id,
                'name' : user.username,
                'image' : s.data['image_memory'],
                'msg' : 'success',
            }
       
        if (user.isemailvalid==True):
            return response
        return Response({
            'msg' : 'user did not validate email',
            'detail': 0,
            'name' : 'NA',
            'image' : 'NANA',
        })


        
       

        
       

        
        

        
    

        


       
class ProfileView(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        user = User.objects.get(pk=user_id)
        if user is None:
            return Response({
            
            'msg' : 'User not found !',
            
        })
        s = UserSerializer(user)



        return Response(
            s.data
        )

    def put(self,request,*args, **kwargs):
        user_id = request.data['userid']
        user = User.objects.get(pk=user_id)

        data = request.data

        user.username = data["username"]
        user.profilepic = data["profilepic"]
        user.email = data['email']

        serializer = UserSerializer(user)
        user.save()
        return Response(serializer.data)





class RegisterPhysicView(APIView):
    def post(self,request):
        # make it impossible for users to have mutliple physic
        user_id = request.data['user_id']
        user = User.objects.get(pk=user_id)
        if user is None:
            return Response({
            
            'msg' : 'User not found !',
            
        })
        physic = Physic.objects.filter(user=user).first()
        s = PhysicSerializer(physic)
        return Response(s.data)

       

    def put(self,request):
         user_id = request.data['user_id']
         height = request.data['height']
         weight = request.data['weight']
         weight_goal = request.data['weight_goal']
         duration = request.data['duration']
         goal = request.data['goal']
         datea = datetime.date.today()
         
         
         
         obj = Physic.objects.get(user=user_id)
         
         obj.height.append(height)
         obj.height_timestamp.append(datea)
         
         
         obj.weight.append(weight)
         obj.weight_timestamp.append(datea)
         obj.weight_goal = weight_goal
         obj.duration = duration
         obj.goal = goal
         obj.save()


         
         

         return Response({'msg' : 'Your update has been saved !'})
         



    def get(self,request):
        
        user = User.objects.filter(pk=2).first()
        s = UserSerializer(user)
        physic = Physic.objects.filter(user=2).first()
        s2 = PhysicSerializer(physic)

        return Response({
            'user' : s.data,
            'physic' : s2.data
            })

class getinfochart(APIView):
    def post(self,request):
        user_id = request.data['user_id']

        physic_height = Physic.objects.filter(user=user_id).values('height')
        list_height = [item["height"] for item in physic_height]

        physic_weight = Physic.objects.filter(user=user_id).values('weight')
        list_weight = [item["weight"] for item in physic_weight]


        list_height_time = Physic.objects.filter(user=user_id).values('height_timestamp')
        list_height_time_true = [item["height_timestamp"] for item in list_height_time]
        days_overdue = [(date.today() - i).days for i in list_height_time_true[0]]


        list_weight_time = Physic.objects.filter(user=user_id).values('weight_timestamp')
        list_weight_time_true = [item["weight_timestamp"] for item in list_weight_time]
        days_overdue2 = [(date.today() - i).days for i in list_height_time_true[0]]

        lista = list(zip(days_overdue2, list_weight[0]))
        
        print(lista)


        weight_goal =  Physic.objects.filter(user=user_id).values('weight_goal')
        weight_goal2 = [item["weight_goal"] for item in weight_goal][0]

        duration = Physic.objects.filter(user=user_id).values('duration')
        duration2 = [item["duration"] for item in duration][0]

        age = User.objects.filter(pk=user_id).values('age')
        age2 = [item["age"] for item in age][0]

        

       

        
        
        return Response({
            'height_days' : days_overdue,
            'weight_days' : days_overdue2,
            'physic_height' : list_height[0],
            'physic_weight' : list_weight[0],
            'list' : lista    ,    
            'weight_goal'  : weight_goal2   ,
            'duration' : duration2,
            'age' : age2,
            
           

            
        })
        #days_overdue =   ( list_height_time_true[0][0] - date.today()).days ,

class PrefView(APIView):
    def post(self,request):
        s = PreferencesSerializer(data = request.data)
        if s.is_valid() :
            s.save()
            return Response(s.data)
        return Response({'msg' : 'error'})



class UserView(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        
        user = User.objects.filter(pk=user_id).first()
        if user is None:
            return Response({'msg' : 'user does not exist'})
        
        s = UserSerializer(user)

        physic = Physic.objects.filter(user=user_id).first()
        s2 = PhysicSerializer(physic)

        preferences = Preferences.objects.filter(user=user_id).first()
        s3 = PreferencesSerializer(preferences)

        list = [s.data,s2.data,s3.data]

        return Response(list)

class MealView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        s = MealSerializer(data=request.data)
        if s.is_valid() :
            s.save()
            return Response(s.data)
        return Response({'msg' : 'error'})
    
    def get(self,request):
        Meals = Meal.objects.all()
        meals_list = list(Meals)
        random.shuffle(meals_list)
        s = MealSerializer(meals_list[:100],many=True)

        return Response({'msg':s.data})

# Create your views here.



# udpate user pref

class UpdateUserPrefView(APIView):
    def put(self,request):
        #pref_id = request.data['pref_id']
        user_id = request.data['user_id']
        user = User.objects.get(pk=user_id)
        if user is None:
            raise AuthenticationFailed('User not found!')
        
        pref = Preferences.objects.get(user=user_id)
        
        
        serializer = PreferencesSerializer(pref,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self,request):
        user_id = request.data['user_id']
        pref = Preferences.objects.get(user=user_id)
        if pref is None:
            return Response({'msg' : 'Pref does not exist'})
        
        s = PreferencesSerializer(pref)
        return Response(s.data)

class OneMealPageView(APIView):
    def post(self,request):
        meal_id = request.data['meal_id']
        meal = Meal.objects.get(pk=meal_id) if Meal.objects.filter(pk=meal_id).exists() else None
        
            
        
        s = MealSerializer(meal)
        return Response(s.data)

        
class  MealQueryView(APIView):
    def post(self,request):

        foodname = request.data['foodname']
        meals = Meal.objects.filter(name__icontains = foodname)[:100]
        s = MealSerializer(meals,many=True)
        
        return Response({'msg' : s.data})

class IngredientsQueryView(APIView):
    def post(self,request):

        ingredients = request.data['ingredients']
        meals = Meal.objects.filter(ingredients__contains=[ingredients])[:100]
        s = MealSerializer(meals,many=True)

        return Response({'msg' : s.data})

class IngredientsOnlyQueryView(APIView):
    def post(self,request):

        ingredients = request.data['ingredients']

        query = Q()
        for ingredient in ingredients:
             query |= Q(ingredients__contains=[ingredient])
        
        s = MealSerializer(query,many=True)
            


        

       
        return Response({'msg' : s.data})




class RateMealView(HttpResponse,APIView):

    def post(self, request):
        user_id = request.data['user_id']
        meal_id = request.data['meal_id']
        rating = request.data['rating']

        user = User.objects.get(pk=user_id)
        meal = Meal.objects.get(pk=meal_id)

        try:
            r = ratings.objects.get(meal=meal_id, user=user_id)
        except ObjectDoesNotExist:
            rating = ratings.objects.create(
                user=user,
                meal=meal,
                rating=rating
            )
            
            testThread(user_id).start()
            return Response({'msg': 'thank you for rating !'})

        r = ratings.objects.filter(meal=meal_id, user=user_id).update(rating=rating)
        testThread(user_id).start()

        return Response({'msg': 'your update has been saved !'})   

class  firstRatingView(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        meal_id = request.data['meal_id']
        rating = request.data['rating']
        user = User.objects.get(pk=user_id)
        meal = Meal.objects.get(pk=meal_id)

        try:
            r = ratings.objects.get(meal=meal_id, user=user_id)
        except ObjectDoesNotExist:
            rating = ratings.objects.create(
                user=user,
                meal=meal,
                rating=rating
            )
            
            testThread(user_id).start()
            user.isnexuser = True
            user.save()
            return Response({'msg': 'thank you for rating !'})

        r = ratings.objects.filter(meal=meal_id, user=user_id).update(rating=rating)
        testThread(user_id).start()
        user.isnexuser = True
        user.save()

        return Response({'msg': 'your update has been saved !'})   
          
        
        
 
           
        
        

def get_similar_food(food_name,user_ratings):
    item_similarity_df = pd.read_csv('corr.csv',index_col=0)
    
    

    similar_score = item_similarity_df[food_name]*(user_ratings-2.5)
    
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score


def updatereco(user_id):
     rating_list = ratings.objects.filter(user=user_id)
     meal_ids = [rating.meal.id for rating in rating_list]
     meal_ratings = rating_list.values('rating').reverse()
     meal_name = Meal.objects.filter(pk__in=meal_ids).values('name')
     print(meal_name)

     name_list = [item["name"] for item in meal_name]
     ratings_list = [item["rating"] for item in meal_ratings]

        

     list_food_reco = list(zip(name_list,ratings_list))
        


        

     similar_food = pd.DataFrame()
       

     for name,rating in list_food_reco:
         similar_food = similar_food.append(get_similar_food(name,rating),ignore_index=True)
    
     df1 = similar_food.sum().sort_values(ascending=False)
     print('test')
     r = User.objects.filter(pk=user_id).update(recomeal = df1.index.tolist())

class Workout(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        user_lists = workout.objects.get(user=user_id)
        return Response({
            'workout_list' : user_lists.workout_list,
            'workout_names' : user_lists.workout_names
        })

class testView(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        updatereco(user_id)
        return Response({'msg':'sucess'})
    def get(self,request):
        meal_list = User.objects.filter(pk=4).values('recomeal')
        print(meal_list)
        meal_list2 = meal_list[0]['recomeal']
        
        

        indexes_mapping = {index: i for i, index in enumerate(meal_list2)}
        meals = Meal.objects.filter(name__in=meal_list2).annotate(
        sort_index=Case(
        *[When(name=name, then=indexes_mapping[name]) for name in meal_list2],
        default=999999999,
            )
        ).order_by('sort_index')

        sm = MealSerializer(meals,many=True)
                

       
        
        return Response(sm.data)


        


class RecomendedMealView(APIView):

    
    
       
    
    
    def post(self,request):
        user_id = request.data['user_id']
        meal_list = User.objects.filter(pk=user_id).values('recomeal')
        
        meal_list2 = meal_list[0]['recomeal']
        meal_list2 = meal_list2
        
        

        indexes_mapping = {index: i for i, index in enumerate(meal_list2)}
        meals = Meal.objects.filter(name__in=meal_list2).annotate(
        sort_index=Case(
        *[When(name=name, then=indexes_mapping[name]) for name in meal_list2],
        default=999999999,
            )
        ).order_by('sort_index')[:100]
        meals_list = list(meals)
        random.shuffle(meals_list)
        sm = MealSerializer(meals_list,many=True)
                

       
        
        return Response({'msg' : sm.data})


class OpenAIView(APIView):
    def post(self,request):

        data2 = request.data['user_prompt']
        pre_text = 'give me one meal recommendation based on that, give me only the name nothing else :'

        post_test = 'I want this in the following information : name of the meal , list of ingredients and calories'

        user_input = pre_text + data2 
        print(user_input)

        API_KEY = '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'
        openai.api_key = API_KEY
        model = 'text-davinci-003'
        ######################################## food_name ############################################
        response = openai.Completion.create(
            prompt = user_input,
            model = model

        )
        print(response.usage.total_tokens)

        for result in response.choices:
            answer = result.text
        
        answer = answer.replace('\r', '').replace('\n', '')

        print(answer)

        ############################################### ingredients ##############################
        pre_ingredients = 'what are the ingredients for the following meal ? '
        post_indredients = 'separate ingredients with a "," '
        ingredients_inputs = pre_ingredients + answer + post_indredients


        response_ingredients = openai.Completion.create(
            prompt = ingredients_inputs,
            model = model

        )
        
        for result_ingredients in response_ingredients.choices:
            ingredients = result_ingredients.text
        
        ingredients2 = ingredients.replace('\r', '').replace('\n', '')
        ingredients2 = ingredients2.split(",")
        print(ingredients2)




        ################################################## image #################################
        response_image = openai.Image.create(
            prompt=answer,
            n=1,
            size="256x256"
            )
        image_url = response_image['data'][0]['url']

        ################################################Nutri values##################################

        pre_nutri = 'Give me the values of calories, fat, sugar and protein for 100g for the following meal : '
        post_nutri = 'I want only the numerical values of each separated by ","'
        nutri_inputs = pre_nutri + answer + post_nutri


        response_nutri = openai.Completion.create(
            prompt = nutri_inputs,
            model = model

        )
        
        for result_nutri in response_nutri.choices:
            nutri_values = result_nutri.text
        
        nutrivalueslist = nutri_values.replace('\r', '').replace('\n', '')
        print(nutrivalueslist)
        nutrivalueslist = nutrivalueslist.replace('g', '')
        
        
        nutrivalueslist = nutrivalueslist.replace('k', '').replace('c','').replace('a','').replace('l','').replace('o','').replace('r','').replace('i','').replace('e','').replace('e','').replace('s','').replace('f','').replace('t','').replace('p','').replace('n','').replace('u','').replace(':','').replace('C','').replace('F','').replace('P','').replace('S','').replace('m','')
        #print(list(filter(lambda i: i.isdigit(), nutrivalueslist)))
        print(nutrivalueslist)
        
        nutrivalueslist = nutrivalueslist.split(",")
        if '' in nutrivalueslist:
                nutrivalueslist = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]
        if ' ' in nutrivalueslist:
                nutrivalueslist = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]
        print(nutrivalueslist)
        #nutrivalueslist = [eval(i) for i in nutrivalueslist]
        print(nutrivalueslist)

        if (len(nutrivalueslist) != 4 ):
            nutrivalueslist = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]

        ###################################################### description ###########################
        pre_desc = 'Give me a detailed description for this meal : '
        post_desc = 'I want at least 80 words for the description'
        desc_inputs = pre_desc + answer  


        response_desc = openai.Completion.create(
            max_tokens = 500,
            prompt = desc_inputs,
            model = model

        )
        
        for result_desc in response_desc.choices:
            description = result_desc.text

        description = description.replace('\r', '').replace('\n', '')
        
        

        return Response ({
            'name' : answer,
            'image_url' : image_url,
            'ingredients' : ingredients2,
            'description' : description,
            'nutri_values' : nutrivalueslist,
            
            })






class OpenAIPopulate(APIView):
    def get(self,request):
        API_KEY = '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'
        openai.api_key = API_KEY
        model = 'text-davinci-003'

        pre_text = 'Give me the values of calories, fat, sugar and protein separated by "," of the following meal : '

        post_text = 'Output only numbers, no letters separated by ","'

        
        for i in range(5193, 8000):
            print(i)

            meal = Meal.objects.filter(pk=i+1).values('name')
            name  = meal[0]['name']
            
            user_input = pre_text + name 
            
            ######################################## food_name ############################################
            response = openai.Completion.create(
                prompt = user_input,
                model = model,
                temperature =  0,

            )
            print(response.usage.total_tokens)

            for result in response.choices:
                answer = result.text

            print(answer)
            
            answer = answer.replace('\r', '').replace('\n', '')

            answer = answer.replace('k', '').replace('c','').replace('a','').replace('/','').replace('l','').replace('o','').replace('r','').replace('i','').replace('e','').replace('e','').replace('s','').replace('f','').replace('t','').replace('p','').replace('n','').replace('u','').replace(':','').replace('C','').replace('F','').replace('P','').replace('S','').replace('m','').replace('g','').replace('v','').replace('w','').replace('h','').replace('d','').replace('b','').replace('q','').replace('j','').replace('x','').replace('y','').replace('z','').replace('U', '').replace('A', '').replace('B', '').replace('C', '').replace('D', '').replace('E', '').replace('F', '').replace('G', '').replace('H', '').replace('I', '').replace('J', '').replace('K', '').replace('L', '').replace('M', '').replace('N', '').replace('O', '').replace('P', '').replace('Q', '').replace('R', '').replace('S', '').replace('T', '').replace('V', '').replace('W', '').replace('X', '').replace('Y', '').replace('Z', '')

            answer = answer.replace('\r', '').replace('\n', '')
            print(answer)
            answer = answer.split(",")
            print(answer)
            if '' in answer:
                answer = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]
            if ' ' in answer:
                answer = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]
            if '  ' in answer:
                answer = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]
            if '  ' in answer:
                answer = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]
            if '   ' in answer:
                answer = [str(random.randint(200, 500)),str(random.randint(2, 33)),str(random.randint(2, 33)),str(random.randint(2, 33))]

            meal = Meal.objects.filter(pk=i+1).update(nutri_values=answer)
            r = random.randint(1,2)
            time.sleep(2)
           
                


        
        


        return Response({'msg': 'success'} )

class OpenAIName(APIView):
    def post(self,request):
        data2 = request.data['user_prompt']
        
        
        API_KEY = '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'
        openai.api_key = API_KEY
        model = 'text-davinci-003'

        for i in range(6519,7000):

            meal = Meal.objects.filter(pk=i).values('name')
            name  = meal[0]['name']
            print(name)


            user_input = 'output only the name of this meal :' +   name 


            response = openai.Completion.create(
                prompt = user_input,
                model = model

            )
            
           
            #print(response.usage.total_tokens)

            for result in response.choices:
                answer = result.text
            

            answer = answer.replace('\r', '').replace('\n', '')
            meal = Meal.objects.filter(pk=i).update(name=answer)
            print(answer)
            print('')
            time.sleep(5)

        return Response({'msg': 'success'})


def pad_lists(list_of_lists):
    max_length = max(len(lst) for lst in list_of_lists)
    padded_list_of_lists = [lst + ['None'] * (max_length - len(lst)) for lst in list_of_lists]
    return padded_list_of_lists


class OpenAISport(APIView):
    def post(self,request):
        user_id = request.data['user_id']
        nbr_workout = request.data['nbr_workout']
        user = User.objects.get(pk=user_id)
        user_physic = Physic.objects.filter(user=user_id)
        
        personal_info = ''
        
        query = 'Recommend me a sports program based on the following information about me :'
        weight_s = user_physic.values('weight')
        weight  = weight_s[0]['weight'][-1]
        print(weight)
        height_s = user_physic.values('height')
        height  = height_s[0]['height'][-1]
        print(height)

        goal = user_physic.values('weight_goal')
        goal = goal[0]['weight_goal']
        print(goal)
        goal_string = ''

        if(goal < weight):
            goal_string = 'losing weight'
        elif(goal == weight):
            goal_string = 'keep the same weight'
        elif(goal > weight):
            goal_string = 'gaining weight'
        
        personal_info = 'age:' + str(user.age) + ';goal:' + str(goal_string) + ';weight:' + str(weight) +';height:' + str(height)  + ';number of workout:' + str(nbr_workout)

        print(personal_info)

        user_input = query + personal_info
        

        API_KEY = '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'
        openai.api_key = API_KEY
        model = 'text-davinci-003'

        user_info = "age:21;goal:losing weight;weight:80;height:180cm;number of workout:5"

        response = openai.Completion.create(
                    prompt = 'recommender me a detailed workout program for a user based on this information' + personal_info + 'I want you to output me : day x - name of wourkout : bullet point of the workout'"?{}",
                    model = model,
                    temperature = 0.8,
                    max_tokens = 500,
                    
                    top_p=  1,
                    frequency_penalty= 0,
                    presence_penalty= 0,
                    stop= ['{}'],
                )

        print(response.usage.total_tokens)

        for result in response.choices:
            answer = result.text


        import re
        print(answer)
       



       
        days = re.split(r'\n+Day \d+ - ', answer)[1:]

        # Iterate over each day and extract its workouts
        wowo =[]
        workout_names = []
        for day in days:
            lines = day.strip().split('\n')
            workouts = [line.strip() for line in lines[1:]]
            new_list = [s.replace('•', '-') for s in workouts]
           
            wowo.append(new_list)
            workout_name = day.strip().split(':')[0]
            workout_names.append(workout_name)
            
        
        print(wowo)
        print('hhhhhhhhhhhhhh')
        print(workout_names     )
        wowo2 = pad_lists(wowo)

        
        #workout_profile = workout.objects.filter(user=user)
        workout_profile = workout.objects.filter(user=user).update(workout_names = workout_names,workout_list=wowo2)
        
        
        
        

        # Print the exercise list for the third workout
        #print(splittest)

        return Response({
            'list_workout' : wowo,
            'list_name' : workout_names
        })




'''''''''
 user_id = request.data['user_id']
        rating_list = ratings.objects.filter(user=user_id)
        meal_ids = [rating.meal.id for rating in rating_list]
        meal_ratings = rating_list.values('rating').reverse()
        meal_name = Meal.objects.filter(pk__in=meal_ids).values('name')
        print(meal_name)

        name_list = [item["name"] for item in meal_name]
        ratings_list = [item["rating"] for item in meal_ratings]

        

        list_food_reco = list(zip(name_list,ratings_list))
        


        

        similar_food = pd.DataFrame()
       

        for name,rating in list_food_reco:
           similar_food = similar_food.append(get_similar_food(name,rating),ignore_index=True)    

        
        df1 = similar_food.sum().sort_values(ascending=False)
        print(df1.index)
        
        indexes = np.random.permutation(df1.index)
        df1 = df1.reindex(indexes)
        #print(df1.index)
       # the query list them by id
        
        indexes_mapping = {index: i for i, index in enumerate(df1.index)}
        meals = Meal.objects.filter(name__in=df1.index).annotate(
        sort_index=Case(
        *[When(name=name, then=indexes_mapping[name]) for name in df1.index],
        default=999999999,
            )
        ).order_by('sort_index')
                
        sm = MealSerializer(meals,many=True)
        
        
        
        return Response({'msg':sm.data})

'''''''''''
