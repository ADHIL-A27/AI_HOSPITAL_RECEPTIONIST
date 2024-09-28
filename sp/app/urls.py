from django.urls import path
from .views import hello_world,send_message

urlpatterns = [
    path('', hello_world, name='hello_world'),  # Added name for clarity
    path('send-message/', send_message, name='send_message'),
]
