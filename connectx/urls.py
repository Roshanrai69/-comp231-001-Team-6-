from django.urls import path
from .views import login_view

urlpatterns = [
    path('', login_view, name='login'), # add this line
    path('login/', login_view, name='login'),
]
