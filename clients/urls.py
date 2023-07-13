from django.urls import include, path
from . import views


from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('api/clients/', views.UserList.as_view()),
    path('api/clients/create/', views.UserCreate.as_view()),
    path('', include(router.urls)),
]