import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vault.settings')

from django.core.management import execute_from_command_line
execute_from_command_line(['', 'check'])

from locust import HttpUser, task, between
from django.urls import reverse

class DjangoUser(HttpUser):
    host = "http://127.0.0.1:8000" 
    wait_time = between(1, 2)

    @task
    def test_project_onemeal_POST(self):
        onemeal_url = reverse('onemeal')

        # Print the generated URL to check if it's correct
        print("URL:", onemeal_url)

        # Replace 'meal_id' and '2' with the appropriate POST data for your view
        response = self.client.post(onemeal_url, {
            'meal_id': 2
        })

    
    @task
    def test_meal_view_GET(self):
        self.client.get("/api/meal")
