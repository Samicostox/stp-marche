import threading
from time import sleep
import pandas as pd



from .models import *




class testThread(threading.Thread):

    def __init__(self,user_id):
        self.user_id = user_id
        super(testThread, self).__init__()

    


    
    def run(self):
        def get_similar_food(food_name,user_ratings):

            item_similarity_df = pd.read_csv('corr.csv',index_col=0)
            
            

            similar_score = item_similarity_df[food_name]*(user_ratings-2.5)
            
            similar_score = similar_score.sort_values(ascending=False)
            return similar_score

        try:
            rating_list = ratings.objects.filter(user=self.user_id)
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
            r = User.objects.filter(pk=self.user_id).update(recomeal = df1.index.tolist())
            print('done')
           

        except Exception as e:
            print(e)
        
        