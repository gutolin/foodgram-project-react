from rest_framework import filters, permissions, status, viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, api_view, permission_classes

from user.serializers import UserSerializer, UserAccessSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = UserAccessSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)