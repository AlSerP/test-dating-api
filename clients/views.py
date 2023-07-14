from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from . import models


User = get_user_model()


class LoginView(APIView):
    """
    User login by email and password.
    """

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
  
    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)


class UserList(APIView):
    """
    List users with query filters.
    """

    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get(self, request):
        print(User.objects.get(id=30).get_distance_to(User.objects.get(id=31)))
        FILTER_PARAMS = ['first_name', 'last_name', 'is_male']

        filter_settings = {}
        for param in FILTER_PARAMS:
            param_value = self.request.query_params.get(param)
            if param_value:
                filter_settings[param] = param_value

        queryset = User.objects.all().filter(**filter_settings)

        max_distance_value = float(self.request.query_params.get('max_distance'))
        if max_distance_value:
            for user in queryset:
                distance = request.user.get_distance_to(user)
                if distance > max_distance_value: 
                    queryset = queryset.exclude(id=user.id)

        serializer_for_queryset = UserSerializer(instance=queryset, many=True)

        return Response(serializer_for_queryset.data)
    
    def get_queryset(self):
        return User.objects.all()


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


class UserMatch(APIView):
    """
    Send a match from <id> user to another user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        print(request.data)
        
        if not User.objects.filter(pk=id).exists():
            return Response({"error": "There is no such User"}, status=status.HTTP_400_BAD_REQUEST)

        if int(id) == request.user.id:
            return Response({"error": "You are perfect, but you can not match yourself"}, status=status.HTTP_400_BAD_REQUEST)

        user_from = request.user
        target = User.objects.get(pk=id)

        response = user_from.match(target)

        if response.get('error', None):
            return Response({'error': response['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_201_CREATED)
