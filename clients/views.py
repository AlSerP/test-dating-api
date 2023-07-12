from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer

class AllUserView(APIView):
    def get(self, request):
        User = get_user_model()
        queryset = User.objects.all()
        serializer_for_queryset = UserSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)
