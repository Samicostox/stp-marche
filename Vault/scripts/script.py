from main.models import Meal
import csv


def run():
    with open("final_meal.csv", encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Meal.objects.all().delete()
        

        for row in reader:
            print(row)

            

            meal = Meal(recipe_id=row[0],
                        name=row[1],
                        description=row[2],
                        ingredients=row[3],
                        steps=row[4],
                        nutri_values=row[5],
                        foodpic=row[6],
                        n_steps=row[7],
                        tags=row[8],
                        rating=row[9],)
            meal.save()