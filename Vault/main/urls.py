from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('register', RegisterView.as_view(),name='register'),
    path('physic', RegisterPhysicView.as_view()),
    path('pref', PrefView.as_view()),
    path('user', UserView.as_view()),
    path('login',LoginView.as_view(),name='login'),
    path('meal',MealView.as_view(),name='meal'),
    path('pref_info',UpdateUserPrefView.as_view()),
    path('profile',ProfileView.as_view(),name = 'profile'),
    path('onemeal',OneMealPageView.as_view(),name='onemeal'),
    path('test',testView.as_view()),
    path('email_verify', VerifyEmail.as_view(), name="email_verify"),
    path('emailPage', EmailPageView.as_view()),
    path('mealquery', MealQueryView.as_view()),
    path('rate', RateMealView.as_view()),
    path('reco', RecomendedMealView.as_view(),name='reco'),
    path('firstrating', firstRatingView.as_view()),
    path('charts', getinfochart.as_view()),
    path('ingredientsquery',IngredientsQueryView.as_view()),
    path('ingredientsonlyquery',IngredientsOnlyQueryView.as_view()),
    path('openai',OpenAIView.as_view()),
    path('openai_populate',OpenAIPopulate.as_view(),name='openai_populate'),
    path('openai_populate_name',OpenAIName.as_view()),
    path('openai_sports',OpenAISport.as_view()),
    path('workout',Workout.as_view()),

]
