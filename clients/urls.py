from django.urls import include, path
from . import views

urlpatterns = [
    path('list/', views.UserList.as_view()),
    path('login/', views.LoginView.as_view()),
    path('clients/create/', views.UserCreate.as_view()),
    path('clients/<id>/match/', views.UserMatch.as_view())
]
