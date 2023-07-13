from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('create/', views.UserCreate.as_view()),
    path('<id>/match/', views.UserMatch.as_view())
]
