from api.models import Follow
from api.serializers import FollowSerializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = IsAuthenticated

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """Функция обрабатывающая запросы на создание/удаление
        подписки на автора."""
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if request.method == 'DELETE':
            if user == author:
                return Response({
                    'errors': 'Вы не можете отписываться от самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({
                'errors': 'Вы уже отписались'
            }, status=status.HTTP_400_BAD_REQUEST)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.get_or_create(user=user, author=author)
        serializer = FollowSerializers(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
