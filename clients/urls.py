from django.urls import include, path
from . import views


urlpatterns = [
    path('api/clients/', views.UserList.as_view()),
    path('api/clients/create/', views.UserCreate.as_view()),
]