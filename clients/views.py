from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserList(APIView):
    """
    List users with query filters.
    """
    def get(self, request):
        FILTER_PARAMS = ['first_name', 'last_name', 'is_male']

        filter_settings = {}
        for param in FILTER_PARAMS:
            param_value = self.request.query_params.get(param)
            if param_value:
                filter_settings[param] = param_value

        queryset = User.objects.all().filter(**filter_settings)
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


class UserMatch(APIView):
    """
    Send a match from <id> user to another user.
    """
    def post(self, request, id):
        print(request.data)

        target_id = request.data.get('user_id', None)
        if not target_id:
            return Response({"user_id": "Required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(pk=id).exists() or not User.objects.filter(pk=target_id).exists():
            return Response({"error": "There is no such User"}, status=status.HTTP_400_BAD_REQUEST)

        if int(id) == int(target_id):
            return Response({"error": "You are perfect, but you can not match yourself"}, status=status.HTTP_400_BAD_REQUEST)

        user_from = User.objects.get(pk=id)
        target = User.objects.get(pk=target_id)

        response = user_from.match(target)

        if response.get('error', None):
            return Response({'error': response['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_201_CREATED)
