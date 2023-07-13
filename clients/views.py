from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer


class UserList(APIView):
    """
    List all users.
    """
    def get(self, request):
        User = get_user_model()
        queryset = User.objects.all()
        serializer_for_queryset = UserSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)


class UserCreate(APIView):
    """
    Create new user.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
