from django.urls import path
from .views import chatroom
app_name="chatroom"
urlpatterns = [
    path('chatroom/<str:username>/', chatroom, name='chatbox'),
]
