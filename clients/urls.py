from django.urls import include, path
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'users', views.AllUserView)

urlpatterns = [
    # path('', include(router.urls)),
    path('api/clients/', views.AllUserView.as_view()),
]