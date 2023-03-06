from django.db.models import F

from main.models import Meal

# Assuming your model is called "Recipe"
def run():
    recipes = Meal.objects.all()

    for recipe in recipes:
        recipe.steps = [step.replace("'", "") for step in recipe.steps]
        recipe.save()
        